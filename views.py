import datetime, math
from __init__ import app, db, models
import helpers
from flask import render_template, flash, redirect, url_for, request, Response
from sqlalchemy import desc, extract

@app.route('/')
@app.route('/index')
def index():
	latest = models.post.query.filter(models.post.show_number).filter(models.post.date < datetime.datetime.utcnow()).order_by(models.post.show_number).all()[-1]
	return render_template('home.html',latest=latest)

@app.route('/posts')
@app.route('/posts/<year>/<month>/<day>/<title>')
def posts(year=None, month=None, day=None, title=None):
	if title:
		posts = models.post.query.filter(models.post.title == title.replace('_',' ')).filter(extract('year',models.post.date)==year).filter(extract('month',models.post.date)==month).filter(extract('day',models.post.date)==day).all()
		if len(posts) != 0:
			return render_template('posts.html', posts=posts)
	posts = models.post.query.filter(models.post.date < datetime.datetime.utcnow()).order_by(desc(models.post.date)).all()
	if request.args.get('format')=='rss':
		date=helpers.format_date_rss(datetime.datetime.utcnow())
		for post in posts:
			post.itunes_date = helpers.format_date_rss(post.date)
		return Response(render_template('rss.xml', date=date, posts=posts), mimetype='text/xml')
	else:
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
		return render_template('posts.html', posts=posts, numpages=numpages, current_page=current_page)
		
@app.route('/submit')
def submit():
	
	return render_template('submit.html')
	
@app.route('/about')
def about():
    return render_template('about.html')
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404