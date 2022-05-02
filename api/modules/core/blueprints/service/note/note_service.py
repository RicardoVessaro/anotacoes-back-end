
import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from api.modules.core.blueprints.service.note.note_validator import NoteValidator
from api.modules.core.blueprints.service.tag.tag_service import OK
from arq.service.crud_service import CRUDService

CREATED_IN = 'created_in'
TAG = 'tag'

class NoteService(CRUDService):

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
            body[TAG] = OK.id

        return super().insert(body)