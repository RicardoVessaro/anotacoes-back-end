
from ipsum.data.cascade import Cascade
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from api.annotation.data.model.picture import Picture
from api.annotation.data.dao.comment_dao import CommentDAO

class PictureDAO(DetailCRUDDAO):

    model_name = 'Picture'

    def __init__(self) -> None:
        super().__init__(
            model=Picture,
            cascade=Cascade(
                childs=[
                    CommentDAO()
                ]
            )
        )
