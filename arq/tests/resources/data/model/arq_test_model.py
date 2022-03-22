from mongoengine import Document, StringField, IntField, BooleanField, ListField

class ArqTestModel(Document):

    code = IntField()

    title = StringField()

    boolean = BooleanField()

    tags = ListField(StringField())


