
import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from api.modules.core.blueprints.service.note.note_validator import NoteValidator
from arq.service.arq_crud_service import ArqCRUDService

class NoteService(ArqCRUDService):

    def __init__(self) -> None:
        super().__init__(
            dao=NoteDAO(), 
            validator=NoteValidator(), 
            non_editable_fields=['created_in']
        )
    
    def insert(self, body: dict):
        body['created_in'] = datetime.datetime.today()

        return super().insert(body)