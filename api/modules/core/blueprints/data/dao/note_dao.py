
from api.modules.core.blueprints.data.model.note import Note

from arq.data.dao.arq_crud_dao import ArqCRUDDAO

class NoteDAO(ArqCRUDDAO):

    def __init__(self) -> None:
        super().__init__(Note)
    