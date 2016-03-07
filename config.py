#Configures the database information for the website

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Change 'eb.db' if using a different filename
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'eb.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_secret'