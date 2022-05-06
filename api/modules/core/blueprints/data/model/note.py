from api.db import db

class Note(db.Document):

    title = db.StringField()

    pinned = db.BooleanField()

    text =  db.StringField()

    created_in = db.DateTimeField()

    tag = db.ObjectIdField()

    moods = db.ListField(field=db.ObjectIdField())
