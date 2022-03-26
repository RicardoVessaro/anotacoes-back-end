from api.db import db

# TODO Adicionar campo ENUM humor (mood), lista com emojis (para testar enum)
class Note(db.Document):

    title = db.StringField()

    pinned = db.BooleanField()

    text =  db.StringField()

    created_in = db.DateTimeField()
