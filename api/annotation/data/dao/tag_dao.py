
from ipsum.data.dao.crud_dao import CRUDDAO
from api.annotation.data.model.tag import Tag
from ipsum.data.dependent import Dependent
from api.annotation.data.dao.note_dao import NoteDAO

class TagDAO(CRUDDAO):

    model_name = 'Tag'

    def __init__(self) -> None:
        
        dependents = [
            Dependent.Dependency(NoteDAO(), NoteDAO.model_name, 'tag')
        ]

        super().__init__(
            Tag, 
            dependent=Dependent(self.model_name, dependents)
        )