
from ipsum.service.crud_validator import CRUDValidator


class FakeCRUDValidator(CRUDValidator):

    def __init__(self, dao, required_fields=[]) -> None:
        super().__init__(dao, required_fields)
