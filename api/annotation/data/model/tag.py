
from ipsum.data.model.enum_document import EnumDocument
from mongoengine import IntField

class Tag(EnumDocument):

    priority = IntField()
