
from ipsum.service.enum.enum_validator import EnumValidator

class MoodValidator(EnumValidator):

    def __init__(self, dao) -> None:
        super().__init__(dao)
