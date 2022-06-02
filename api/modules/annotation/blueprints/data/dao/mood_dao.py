
from api.modules.annotation.blueprints.data.model.mood import Mood
from arq.data.dao.crud_dao import CRUDDAO

class MoodDao(CRUDDAO):

    def __init__(self) -> None:
        super().__init__(Mood)
