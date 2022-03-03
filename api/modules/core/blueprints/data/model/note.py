from api.db import db

# TODO Adicionar campo humor (mood), lista com emojis (para testar enum) (dps da arquitetura)
class Note(db.Document):

    title = db.StringField()

    pinned = db.BooleanField()

    text =  db.StringField()

    created_in = db.DateTimeField()
