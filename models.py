#models.py - Defines the database tables used in the website. These are used to store information about episodes,
# which is displayed with each post

from __init__ import db

#music_link_table is a two-column table that connects the post table and the music table
#This allows many-to-many relationships, so many posts can use the same song, and many songs can be used in the same post
music_link_table = db.Table('music_link', db.Model.metadata,
    db.Column('id', db.Integer, primary_key = True),
	db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
	db.Column('music_id', db.Integer, db.ForeignKey('music.id'))
)

class music_link(object):
    def __init__(self, post_id, music_id):
        self.post_id = post_id
        self.music_id = music_id

db.mapper(music_link, music_link_table)
db.create_all()

#Every post on the website has an entry in post
#Note that audio files and image files are stored as strings referencing the URL where those files live, not as blobs
#If the post is not an official show, simply don't include an audio_file_location
#date values are date and time, and have no value restrictions. If the stored time is after the time of query, the app considered it "Scheduled to be posted" and won't display it until that time
class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), index=True)
    show_number = db.Column(db.Float, unique=True)
    date = db.Column(db.DateTime())
    audio_file_location = db.Column(db.String())
    image = db.Column(db.String())
    notes = db.Column(db.String(), index=True)
    music = db.relationship("music",secondary=music_link_table, backref="episodes")

    def __repr__(self):
        return '<%r>' % (self.title)

# All music used in episodes should include attribution. This is stored in a separate table to allow easier searching
# This table is connected to the post table via the music_link_table
# This table is connected to the post table via the music_link_table
class music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(), index=True)
    song = db.Column(db.String(), index=True)
    website = db.Column(db.String())

    def __repr__(self):
        return '<Artist: %r><Song: %r>' % (self.artist, self.song)

#A repository of all the taglines we use on the show
#A random one can be selected and displayed underneath the big "Encyclopedia Brunch" banner at the top on each page load
class taglines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagline = db.Column(db.String())


# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username