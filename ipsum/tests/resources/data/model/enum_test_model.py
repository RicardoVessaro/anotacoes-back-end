
from mongoengine import IntField
from ipsum.data.model.enum_document import EnumDocument

class EnumTestModel(EnumDocument):

    integer = IntField()
