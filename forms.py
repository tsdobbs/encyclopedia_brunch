from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateTimeField, TextAreaField, FileField
from wtforms.validators import DataRequired

class submit_ep_form(Form):
    title = StringField('title', validators=[DataRequired()])
    publish_now = BooleanField('publish_now?', default=True)
    date = DateTimeField('publish_date',validators=[DataRequired()],format='%Y-%m-%d %H:%M:%S')
    audio_file_location = StringField('audio_file_location')
    audio_upload = FileField('audio_upload')
    audio_upload_option = BooleanField('upload_audio_to_server?', default=False)
    image = StringField('image')
    image_upload = FileField('image_upload')
    image_upload_option = BooleanField('upload_an_image?', default=False)
    notes = TextAreaField('notes')
    music_artist = StringField('music_artist')
    music_song = StringField('music_song')
    music_website = StringField('music_website')