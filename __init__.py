#__init__.py - imports Flask and SQLALchemy, sets them to variables,
# then imports models.py and views.py, which define the content of the website

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import models, views