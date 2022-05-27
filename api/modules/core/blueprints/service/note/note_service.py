
import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from api.modules.core.blueprints.service.note.note_validator import NoteValidator
from api.modules.core.blueprints.service.tag.tag_service import OK
from arq.service.crud_service import CRUDService
from api.modules.core.blueprints.service.tag.tag_service import TagService

CREATED_IN = 'created_in'
TAG = 'tag'

class NoteService(CRUDService):

    NAME = 'note'

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