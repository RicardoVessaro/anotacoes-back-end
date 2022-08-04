
from api.annotation.data.model.mood import Mood
from api.annotation.data.dao.mood_dao import MoodDao
from api.annotation.service.mood.mood_validator import MoodValidator
from ipsum.service.enum.ipsum_enum import ipsum_enum
from ipsum.service.enum.enum_service import EnumService


COOL = Mood(id='62b356430d2ae186982e96ef', code=1, name='Cool')
OK = Mood(id='62b356430d2ae186982e96f0', code=2, name='Ok')
BORING = Mood(id='62b356430d2ae186982e96f1', code=3, name='Boring')
SAD = Mood(id='62b356430d2ae186982e96f2', code=4, name='Sad')
LOVE = Mood(id='62b356430d2ae186982e96f3', code=5, name='Love')
GREAT = Mood(id='62b356430d2ae186982e96f4', code=6, name='Great')

@ipsum_enum()
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
