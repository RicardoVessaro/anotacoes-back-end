
from api.annotation.data.model.mood import Mood
from ipsum.data.dao.crud_dao import CRUDDAO

class MoodDao(CRUDDAO):

    def __init__(self) -> None:
        super().__init__(Mood)
