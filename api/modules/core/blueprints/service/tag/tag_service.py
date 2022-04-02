
from api.modules.core.blueprints.data.dao.tag_dao import TagDAO
from api.modules.core.blueprints.data.model.tag import Tag
from api.modules.core.blueprints.service.tag.tag_validator import TagValidator
from arq.service.enum.arq_enum import arq_enum
from arq.service.enum.enum_service import EnumService

@arq_enum()
class TagService(EnumService):

    def __init__(self) -> None:
        enums = [
            Tag(code=1, name="IMPORTANT", priority=1),
            Tag(code=2, name="OK", priority=2),
            Tag(code=3, name="LATER", priority=3)
        ]
        
        dao = TagDAO()

        super().__init__(
            dao=dao, 
            validator=TagValidator(dao), 
            enums=enums
        )
