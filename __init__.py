#__init__.py - imports Flask, SQLALchemy, and Flask-Admin sets them to variables,
# then imports models.py and views.py, which define the content of the website

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app, name='encyclopedia brunch', template_mode='bootstrap3')

import models, views, admin_views