from __init__ import db, models, login_manager, app
from flask import redirect, url_for, request, render_template
from flask_admin import expose, helpers
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from forms import LoginForm, submit_ep_form
import helpers as my_helpers
import flask_login as login
from werkzeug import secure_filename
import os, requests, datetime
from sqlalchemy import desc
import markdown

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

class PostModelView(ModelView):
    column_searchable_list = ['title', 'notes']
    column_filters = ['title', 'date', 'music']

    def is_accessible(self):
        return login.current_user.is_authenticated

class MusicModelView(ModelView):
    column_searchable_list = ['artist', 'song']

    def is_accessible(self):
        return login.current_user.is_authenticated

# Create customized index view class that handles both login/logout and displays the submit new episode form when already logged-in
class AdminSubmitView(AdminIndexView):
    # Much of the form validation and processing is done in this view, and it really should be moved into the form definition
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
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

            # Check what the last episode number was and add one
            this_ep_num = models.post.query.filter(models.post.show_number).order_by(models.post.show_number).all()[-1].show_number + 1

            #Upload audio from user if that box is checked
            form.audio_filepath = False
            if form.data['audio_upload_option']:
                audio_file = request.files['audio_upload']
                if not audio_file.filename: form.errors['audio_upload'] = 'No file selected!'
                audio_filepath = os.path.join(app.config['AUDIO_UPLOAD_FOLDER'], secure_filename(audio_file.filename))
                audio_file.save(audio_filepath)
                form.audio_filepath = audio_filepath[audio_filepath.find('static')-1:]
                if form.data['audio_upload_to_ia_option']:
                    form.audio_filepath = my_helpers.upload_to_ia(audio_filepath, form.data['title'], this_ep_num)
                    os.remove(audio_filepath)

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

            return redirect(url_for('.preview_view'))
        return self.render('admin/submit.html', form=form)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(AdminSubmitView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

    #Preview the post you just made to make sure it looks about how you think it should
    #A better way to do this would be to set up the preview from form variables, then not commit to the db until after the preview
    #   However, the way the session is committed in the submit step above means that it would have to be slightly reworked
    #   This method works for now so that at least the user sees the result before it goes live, if scheduled
    @expose('/preview/', methods=('GET','POST'))
    def preview_view(self):
        post = models.post.query.order_by(desc(models.post.id)).first()
        post.title = 'PREVIEW || ' + post.title + ' || WILL POST ON ' + str(post.date)
        post.html_notes = markdown.markdown(post.notes, extensions=['markdown.extensions.sane_lists','markdown.extensions.nl2br'])
        return self.render('posts.html', posts=[post])


admin = Admin(app, name='encyclopedia brunch', template_mode='bootstrap3', index_view=AdminSubmitView(), base_template='admin/logout.html')
admin.add_view(PostModelView(models.post, db.session))
admin.add_view(MusicModelView(models.music, db.session))