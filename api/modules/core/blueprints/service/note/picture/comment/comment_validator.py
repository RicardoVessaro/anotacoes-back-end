
from arq.service.detail_crud_validator import DetailCRUDValidator

class CommentValidator(DetailCRUDValidator):

    def __init__(self, dao, parent_dao) -> None:
        super().__init__(dao, parent_dao, required_fields=['comment'])
