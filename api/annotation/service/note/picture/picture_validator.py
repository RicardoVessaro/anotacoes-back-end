
from ipsum.service.detail_crud_validator import DetailCRUDValidator

class PictureValidator(DetailCRUDValidator):

    def __init__(self, dao, parent_dao) -> None:
        super().__init__(dao, parent_dao, required_fields=['title'])
