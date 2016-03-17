#views.py - Maps URLs to backend functions, then returns the results to the appropriate view

import datetime, math, markdown, os, requests
from __init__ import app, db, models
import helpers
from flask import render_template, flash, redirect, url_for, request, Response
from sqlalchemy import desc, extract, sql
from forms import submit_ep_form
from werkzeug import secure_filename

#Home page
#Determines what the latest episode is by querying for all episodes, ordered by ascending show number, then takes the last result
#Note that the query filters out any post that is listed as posting after the current time, so it won't show "Scheduled" shows here
@app.route('/')
@app.route('/index')
def index():
    latest = models.post.query.filter(models.post.show_number).filter(models.post.date < datetime.datetime.utcnow()).order_by(models.post.show_number).all()[-1]
    return render_template('home.html',latest=latest)

#Displays posts
#If /posts is requested, queries for all posts, then paginates into sets of 5
@app.route('/posts')
#If a specific post is requested in the format below, displays only that post
@app.route('/posts/<year>/<month>/<day>/<title>')
def posts(year=None, month=None, day=None, title=None):
    #If a year, month, day, and title are given in the URL, queries for that post and, if the query returns something, renders it.
    if title:
        posts = models.post.query.filter(models.post.title == title.replace('_',' ')).filter(extract('year',models.post.date)==year).filter(extract('month',models.post.date)==month).filter(extract('day',models.post.date)==day).all()
        if len(posts) != 0:
            #translate notes from Markdown to HTML. There should only be one post in this case, so here we only translate the first entry in the list
            posts[0].html_notes = markdown.markdown(posts[0].notes)
            return render_template('posts.html', posts=posts)

    #Queries for all posts that have a date before the time of query. Anything with a date after the time of query is considered "Scheduled" and isn't displayed
    posts = models.post.query.filter(models.post.date < datetime.datetime.utcnow()).order_by(desc(models.post.date)).all()

    #If the requested format is RSS, rewrites the dates into the preferred version for RSS, then renders into XML
    if request.args.get('format')=='rss':
        date=helpers.format_date_rss(datetime.datetime.utcnow())
        for post in posts:
            post.itunes_date = helpers.format_date_rss(post.date)
            post.html_notes = markdown.markdown(post.notes)
        return Response(render_template('rss.xml', date=date, posts=posts), mimetype='text/xml')

    else:
        #A bunch of math to figure out what page you're on and what episodes should be displayed on that page
        posts_per_page = 5
        if request.args.get('page'):
            try:
                current_page = int(request.args.get('page'))
            except:
                current_page = 1
        else:
            current_page = 1
        display_end = posts_per_page*current_page
        display_start = display_end - posts_per_page
        numpages = math.ceil(len(posts)/posts_per_page)
        posts = posts[display_start:display_end]
        for post in posts:
            post.html_notes = markdown.markdown(post.notes)
        return render_template('posts.html', posts=posts, numpages=numpages, current_page=current_page)

#Should be used to allow creator to submit a new episode within the browser
@app.route('/submit',methods = ['GET','POST'])
def submit():
    #require password to access, obviously
    #Automate population of music and music_link_table.
    form = submit_ep_form()
    if form.validate_on_submit():
        #Get all of the artist/song/site combos that were entered (an indefinite number), and put into a list of dictionaries for easy access
        form.song_list = list()
        for song_num in range(len(request.form.getlist('music_artist'))):
            song = dict()
            song['artist'] = request.form.getlist('music_artist')[song_num]
            song['song'] = request.form.getlist('music_song')[song_num]
            song['website'] = request.form.getlist('music_website')[song_num]
            form.song_list.append(models.music(**song))

        #Upload audio from user if that box is checked
        form.audio_filepath = False
        if form.data['audio_upload_option']:
            audio_file = request.files['audio_upload']
            audio_filepath = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], secure_filename(audio_file.filename))
            audio_file.save(audio_filepath)
            form.audio_filepath = audio_filepath[audio_filepath.find('static')-1:]

        #Check what the last episode number was and add one
        this_ep_num = models.post.query.filter(models.post.show_number).order_by(models.post.show_number).all()[-1].show_number + 1

        #Upload image from user if that box is checked, otherwise get from online source
        if (form.image.data and not form.image_upload_option.data) or (form.image_upload.data and form.image_upload_option.data):
            image_filepath = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], str(this_ep_num) + '-' + form.data['title'] + '.')
            if form.image_upload_option.data:
                image_file = request.files['image_upload']
                image_filepath += image_file.filename.split('.')[-1]
                image_file.save(image_filepath)
            else:
                image_filepath += form.data['image'].split('.')[-1]
                image_request = requests.get(form.data['image'])
                image_file = open(image_filepath,'wb')
                for chunk in image_request.iter_content(100000):
                    image_file.write(chunk)
                image_file.close()
            form.image_filepath = image_filepath[image_filepath.find('static')-1:]

        #prep dict to be added to DB]
        manual_music_list = list()
        show_data = dict()
        show_data['title'] = form.title.data
        show_data['show_number'] = this_ep_num
        if form.publish_now.data:
            show_data['date'] = datetime.datetime.utcnow()
        else:
            show_data['date'] = form.date.data
        if form.audio_filepath:
            show_data['audio_file_location'] = form.audio_filepath
        elif form.audio_file_location.data:
            show_data['audio_file_location'] = form.audio_file_location.data
        if form.image.data or form.image_upload.data:
            show_data['image'] = form.image_filepath
        show_data['notes'] = form.notes.data
        for song in form.song_list:
            if models.music.query.filter(models.music.artist == song.artist).filter(models.music.song == song.song).all():
                manual_music_list.append(form.song_list.pop(form.song_list.index(song)))
        show_data['music'] = form.song_list
        #add show_data dict to DB
        db.session.add(models.post(**show_data))
        db.session.commit()

        #manually add the relationships between songs that already existed in the song list and the episode we just posted
        #Quite sure this isn't the best way to do it, but it does work.
        if manual_music_list:
            post_id = models.post.query.order_by(desc(models.post.id)).first().id
            for song in manual_music_list:
                music_id = models.music.query.filter(models.music.artist == song.artist).filter(models.music.song == song.song).first().id
                db.session.add(models.music_link(post_id=post_id, music_id=music_id))
            db.session.commit()

        return redirect('/')
    return render_template('submit.html', form=form)

#Access wikipedia to find image suggestions when submitting a new episode
#This is called with AJAX and inserted into the submission page once a title is known
@app.route('/picsuggest/')
@app.route('/picsuggest/<title>')
def picsuggest(title=None):
    if not title: return ""
    images = helpers.get_image_selection(title)
    return render_template('picsuggest.html', images=images)

#Displays the "About The Show" page. Static.
@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404