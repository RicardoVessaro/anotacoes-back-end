
from api.db import db

class Picture(db.Document): 

    parent_field = 'note_id'

    title = db.StringField()

    created_in = db.DateTimeField()

    note_id = db.ObjectIdField()
