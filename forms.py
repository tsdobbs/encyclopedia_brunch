from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, FileField, DateTimeField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.security import check_password_hash
import helpers, models

class submit_ep_form(Form):
    title = StringField('title', validators=[DataRequired()])
    publish_now = BooleanField('publish_now?', default=False)
    date = DateTimeField('publish_date',validators=[DataRequired()],format='%Y-%m-%d %H:%M:%S', default=helpers.check_next_post_date())
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

# Define login and registration forms (for flask-login)
class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise ValidationError('Invalid password')

    def get_user(self):
        return models.db.session.query(models.User).filter_by(username=self.username.data).first()