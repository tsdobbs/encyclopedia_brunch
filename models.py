from __init__ import db

music_link_table = db.Table('music_link', db.Model.metadata,
	db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
	db.Column('music_id', db.Integer, db.ForeignKey('music.id'))
)

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
		
		
class music(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	artist = db.Column(db.String(), index=True)
	song = db.Column(db.String(), index=True)
	website = db.Column(db.String())

	def __repr__(self):
		return '<Artist: %r>' % (self.artist)