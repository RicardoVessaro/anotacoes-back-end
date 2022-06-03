
from ipsum.data.model.enum_document import CODE, NAME, EnumDocument
from ipsum.service.crud_service import CRUDService
from ipsum.util.object_util import is_none_or_empty

class EnumService(CRUDService):

    def __init__(self, dao, validator, enums, non_editable_fields=[]) -> None:
        
        non_editable_fields.extend(CODE)

        super().__init__(dao, validator, non_editable_fields)

        self.enums = enums

    def save_enums(self):
        self.validator.validate_enums(self.enums)

        for enum in self.enums:
            
            db_enum_result = self.find(code=enum.code)

            if is_none_or_empty(db_enum_result):
                self.insert(enum)

            else:
                db_enum = db_enum_result.first()
                enum.id = db_enum.id

                self.update(enum.id, enum)


    def find_by_code(self, code) -> EnumDocument:
        result = self.find(code=code)

        if result is None:
            return None

        return result.first()