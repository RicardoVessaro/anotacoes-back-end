from api.db import db

class Link(db.Document):

    parent_field = 'note_id'

    title = db.StringField()

    href = db.StringField()

    note_id = db.ObjectIdField()
