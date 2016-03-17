from __init__ import admin, db, models
from flask_admin.contrib.sqla import ModelView

class PostModelView(ModelView):
    column_searchable_list = ['title', 'notes']
    column_filters = ['title', 'date', 'music']

class MusicModelView(ModelView):
    column_searchable_list = ['artist', 'song']

admin.add_view(PostModelView(models.post, db.session))
admin.add_view(MusicModelView(models.music, db.session))