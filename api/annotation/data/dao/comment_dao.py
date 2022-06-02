
from arq.data.dao.detail_crud_dao import DetailCRUDDAO
from api.annotation.data.model.comment import Comment

class CommentDAO(DetailCRUDDAO):

    def __init__(self) -> None:
        super().__init__(model=Comment)
