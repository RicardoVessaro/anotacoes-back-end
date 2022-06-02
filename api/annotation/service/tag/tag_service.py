
from api.annotation.data.dao.tag_dao import TagDAO
from api.annotation.data.model.tag import Tag
from api.annotation.service.tag.tag_validator import TagValidator
from arq.service.enum.arq_enum import arq_enum
from arq.service.enum.enum_service import EnumService

IMPORTANT = Tag(code=1, name="IMPORTANT", priority=1)
OK = Tag(code=2, name="OK", priority=2)
LATER = Tag(code=3, name="LATER", priority=3)

@arq_enum()
class TagService(EnumService):   

    NAME = 'tags'

    def __init__(self) -> None:

        enums = [
            IMPORTANT,
            OK,
            LATER
        ]
        
        dao = TagDAO()

        super().__init__(
            dao=dao, 
            validator=TagValidator(dao), 
            enums=enums
        )
