
import datetime
from api.annotation.data.dao.note_dao import NoteDAO
from api.annotation.service.note.note_validator import NoteValidator
from api.annotation.service.tag.tag_service import OK
from ipsum.service.crud_service import CRUDService
from api.annotation.service.tag.tag_service import TagService

CREATED_IN = 'created_in'
TAG = 'tag'

class NoteService(CRUDService):

    NAME = 'notes'

    fields_inserted_by_default = [CREATED_IN]

    def __init__(self) -> None:
        dao = NoteDAO()

        super().__init__(
            dao=dao, 
            validator=NoteValidator(dao), 
            non_editable_fields=[CREATED_IN]
        )
    
    def insert(self, body):
        body[CREATED_IN] = datetime.datetime.today()

        if TAG not in body:
            body[TAG] = TagService().find_by_code(code=OK.code).id

        return super().insert(body)