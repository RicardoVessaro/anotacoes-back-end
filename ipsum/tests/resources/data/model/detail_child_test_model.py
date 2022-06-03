
from mongoengine import Document, StringField, IntField, BooleanField, ListField, ObjectIdField

class DetailChildTestModel(Document):

    parent_field = 'detail_parent_id'

    code = IntField()

    title = StringField()

    boolean = BooleanField()

    tags = ListField(StringField())

    detail_parent_id = ObjectIdField()
