
from collections import namedtuple

from pytest import raises
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import CLASS_MUST_BE_A_SUBCLASS_OF_ENUMSERVICE

from arq.service.enum.enum_service import EnumService


EnumToInsert = namedtuple('EnumToInsert', 'clazz args kwargs')

enums_to_insert = []

def arq_enum(*args, **kwargs):

    def _(clazz):

        if not issubclass(clazz, EnumService):
            raise ArqException(CLASS_MUST_BE_A_SUBCLASS_OF_ENUMSERVICE.format(clazz, EnumService))

        enum_to_insert = EnumToInsert(clazz, args, kwargs)
        enums_to_insert.append(enum_to_insert)

        return clazz

    return _

def save_enums():

    for e in enums_to_insert:
        instance = e.clazz(*e.args, *e.kwargs)
        instance.save_enums()

