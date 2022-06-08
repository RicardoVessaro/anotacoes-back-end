
from api.annotation.data.model.note import Note
from api.annotation.data.dao.link_dao import LinkDAO
from api.annotation.data.dao.picture_dao import PictureDAO
from ipsum.data.cascade import Cascade

from ipsum.data.dao.crud_dao import CRUDDAO

class NoteDAO(CRUDDAO):

    def __init__(self) -> None:
        super().__init__(
            model=Note,
            cascade=Cascade(
                childs=[
                    LinkDAO(),
                    PictureDAO()
                ]
            )
        )
    