#Configures the database information for the website

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Change 'eb.db' if using a different filename
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'eb.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_secret'

AUDIO_UPLOAD_FOLDER = os.path.join(basedir,'static','audio')
ALLOWED_AUDIO_EXTENSIONS = set(['mp3','mp4','aac','wav','flac'])
IMAGE_UPLOAD_FOLDER = os.path.join(basedir,'static','img','post_images')
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])