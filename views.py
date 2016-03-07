#views.py - Maps URLs to backend functions, then returns the results to the appropriate view

import datetime, math, markdown
from __init__ import app, db, models
import helpers
from flask import render_template, flash, redirect, url_for, request, Response
from sqlalchemy import desc, extract
from forms import submit_ep_form

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
	#MARKDOWN - When we change the 'notes' column to be written in markdown, the translation should be done after this line probably. Maaaaybe after the pagination has been figured out, since there'll be fewer posts then?
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
@app.route('/submit')
def submit(methods = ['GET','POST']):
	#require password to access, obviously
	#Automate populating most columns in the post table
	#Automate population of music and music_link_table.
		# Just have a line for that info, probably with a little + button and some javascript to allow additional lines for additional bands.
		# Autofill the first line with BLAMMOS, but allow it to be changed
	form = submit_ep_form()
	images = helpers.get_image_selection(request.args.get('title'))
	return render_template('submit.html', images=images, form=form)

#Displays the "About The Show" page. Static.
@app.route('/about')
def about():
    return render_template('about.html')
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404