from api.db import db

class Comment(db.Document):

    parent_field = 'picture_id'

    comment = db.StringField()

    picture_id = db.ObjectIdField()
