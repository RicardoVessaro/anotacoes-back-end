import imp
from api.db import db

class Note(db.Document):

    #_id, title, pinned, text, created_in

    title = db.StringField()

    pinned = db.BooleanField()

    text =  db.StringField()

    created_in = db.DateTimeField()
