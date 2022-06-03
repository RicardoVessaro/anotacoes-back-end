from mongoengine import Document, StringField, IntField, BooleanField, ListField, DateTimeField

class IpsumTestModel(Document):

    code = IntField()

    title = StringField()

    boolean = BooleanField()

    tags = ListField(StringField())

    day = DateTimeField()


