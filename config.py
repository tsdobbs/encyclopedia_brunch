#Configures the database information for the website

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#Change 'eb.db' if using a different filename
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'eb.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_secret'

#This accounts for if the static images and audio need to be saved somewhere besides the directory where the code is stored.
#It checks the parent directory of the code directory for a folder that matches alternate_path. If it exists, it uses
#it. Otherwise it uses the basedir
alternate_path = "public_html/eb"
if os.path.exists(os.path.join(os.path.split(basedir)[0],alternate_path)):
    static_basedir = os.path.join(os.path.split(basedir)[0],alternate_path)
else:
    static_basedir = basedir

AUDIO_UPLOAD_FOLDER = os.path.join(static_basedir,'static','audio')
ALLOWED_AUDIO_EXTENSIONS = set(['mp3','mp4','aac','wav','flac'])
IMAGE_UPLOAD_FOLDER = os.path.join(static_basedir,'static','img','post_images')
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])