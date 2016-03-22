#__init__.py - imports Flask, SQLALchemy, and Flask-Admin sets them to variables,
# then imports models.py and views.py, which define the content of the website

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

import models, views, admin_views