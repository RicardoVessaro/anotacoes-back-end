
from mongoengine import Document, StringField, IntField, BooleanField, ListField, ObjectIdField

class DetailTestModel(Document):

    parent_field = 'arq_model_id'

    code = IntField()

    title = StringField()

    boolean = BooleanField()

    tags = ListField(StringField())

    arq_model_id = ObjectIdField()
