
from api.annotation.data.dao.tag_dao import TagDAO
from api.annotation.data.model.tag import Tag
from api.annotation.service.tag.tag_validator import TagValidator
from ipsum.service.enum.ipsum_enum import ipsum_enum
from ipsum.service.enum.enum_service import EnumService

IMPORTANT = Tag(id='62df2767730a8633f2fec97f', code=1, name="IMPORTANT", priority=1)
OK = Tag(id='62b3565f0d2ae186982e9746', code=2, name="OK", priority=2)
LATER = Tag(id='62b356600d2ae186982e9747', code=3, name="LATER", priority=3)

@ipsum_enum()
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
