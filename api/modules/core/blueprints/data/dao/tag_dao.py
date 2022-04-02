
from arq.data.dao.crud_dao import CRUDDAO
from api.modules.core.blueprints.data.model.tag import Tag

class TagDAO(CRUDDAO):

    def __init__(self) -> None:
        super().__init__(Tag)