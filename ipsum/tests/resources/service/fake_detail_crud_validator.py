
from ipsum.service.detail_crud_validator import DetailCRUDValidator

class FakeDetailCRUDValidator(DetailCRUDValidator):

    def __init__(self, dao, parent_dao, required_fields=[]) -> None:
        super().__init__(dao, parent_dao, required_fields)
