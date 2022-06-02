
from api.annotation.blueprints.data.model.note import Note

from arq.data.dao.crud_dao import CRUDDAO

class NoteDAO(CRUDDAO):

    def __init__(self) -> None:
        super().__init__(Note)
    