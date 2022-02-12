
import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDao
from api.modules.core.blueprints.service.note.note_validator import NoteValidator

class NoteService:

    def __init__(self) -> None:
        self._dao = NoteDao()
        self._validator = NoteValidator()

    def insert(self, body: dict):
        body['created_in'] = datetime.date.today()
        
        self._validator.validate_insert(body)
        return self._dao.insert(body)


