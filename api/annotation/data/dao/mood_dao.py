
from api.annotation.data.dao.note_dao import NoteDAO
from api.annotation.data.model.mood import Mood
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.data.dependent import Dependent

class MoodDao(CRUDDAO):

    model_name = 'Mood'

    def __init__(self) -> None:

        dependents = [
            Dependent.Dependency(NoteDAO(), NoteDAO.model_name, 'moods')
        ]
        
        super().__init__(
            Mood,
            dependent=Dependent(self.model_name, dependents)
        )
