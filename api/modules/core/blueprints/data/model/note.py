from api.db import db

# TODO Mood n+(Cool, Ok, Boring, Sad, Love, Great)
class Note(db.Document):

    title = db.StringField()

    pinned = db.BooleanField()

    text =  db.StringField()

    created_in = db.DateTimeField()

    tag = db.ObjectIdField()
