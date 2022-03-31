
from arq.data.model.enum_document import CODE, NAME
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import DUPLICATED_ENUM_CODE
from arq.service.crud_validator import CRUDValidator
from arq.util.object_util import is_none_or_empty

# TODO Refatorar validador para nao validar o validate insert/update 2 vezes

class EnumValidator(CRUDValidator):

    def __init__(self, dao, required_fields=[]) -> None:
        required_fields.extend([CODE, NAME])

        super().__init__(dao, required_fields)

    def validate_enums(self, enums):

        for enum in enums:
            self._validate_duplicated_enum(enum, enums)
            #self._validate_enum(enum)
            
    def _validate_duplicated_enum(self, enum, enums):
        count = 0

        for e in enums:
            if enum.code == e.code:
                count += 1

            if count > 1:
                raise ArqException(DUPLICATED_ENUM_CODE.format(enum.code))

    """
    def _validate_enum(self, enum):
        db_enum = self._dao.find(code=enum.code)

        enum_already_exists = not is_none_or_empty(db_enum)

        if enum_already_exists:
            self.validate_update(enum.id, enum)

        else:
            self.validate_insert(enum)
    """