
from mongoengine import Document, StringField, IntField, BooleanField, ListField, ObjectIdField

class DetailTestModel(Document):

    parent_field = 'ipsum_model_id'

    code = IntField()

    title = StringField()

    boolean = BooleanField()

    tags = ListField(StringField())

    ipsum_model_id = ObjectIdField()
