
from api.annotation.data.model.mood import Mood
from api.annotation.data.dao.mood_dao import MoodDao
from api.annotation.service.mood.mood_validator import MoodValidator
from arq.service.enum.arq_enum import arq_enum
from arq.service.enum.enum_service import EnumService


COOL = Mood(code=1, name='Cool')
OK = Mood(code=2, name='Ok')
BORING = Mood(code=3, name='Boring')
SAD = Mood(code=4, name='Sad')
LOVE = Mood(code=5, name='Love')
GREAT = Mood(code=6, name='Great')

@arq_enum()
class MoodService(EnumService):

    NAME = 'moods'

    def __init__(self) -> None:

        enums = [
            COOL,
            OK,
            BORING,
            SAD,
            LOVE,
            GREAT
        ]

        dao = MoodDao()

        super().__init__(
            dao=dao,
            validator=MoodValidator(dao),
            enums=enums
        )
