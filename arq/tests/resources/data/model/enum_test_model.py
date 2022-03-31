
from mongoengine import IntField
from arq.data.model.enum_document import EnumDocument

class EnumTestModel(EnumDocument):

    integer = IntField()
