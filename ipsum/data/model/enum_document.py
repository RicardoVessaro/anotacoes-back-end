from mongoengine import Document, StringField, IntField

CODE = 'code'
NAME = 'name'

class EnumDocument(Document):

    meta = {'allow_inheritance': True}

    code = IntField()
    name = StringField()