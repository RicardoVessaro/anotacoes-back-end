
from ipsum.data.model.enum_document import CODE, NAME
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import DUPLICATED_ENUM_CODE
from ipsum.service.crud_validator import CRUDValidator

class EnumValidator(CRUDValidator):

    def __init__(self, dao, required_fields=[]) -> None:
        required_fields.extend([CODE, NAME])

        super().__init__(dao, required_fields)

    def validate_enums(self, enums):

        for enum in enums:
            self._validate_duplicated_enum(enum, enums)
            
    def _validate_duplicated_enum(self, enum, enums):
        count = 0

        for e in enums:
            if enum.code == e.code:
                count += 1

            if count > 1:
                raise IpsumException(DUPLICATED_ENUM_CODE.format(enum.code))
