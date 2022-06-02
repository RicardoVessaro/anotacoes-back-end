
from arq.data.dao.crud_dao import CRUDDAO
from api.annotation.data.model.tag import Tag

class TagDAO(CRUDDAO):

    def __init__(self) -> None:
        super().__init__(Tag)