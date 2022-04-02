
from arq.service.enum.enum_validator import EnumValidator


class TagValidator(EnumValidator):

    def __init__(self, dao) -> None:
        super().__init__(dao, required_fields= ['priority'])