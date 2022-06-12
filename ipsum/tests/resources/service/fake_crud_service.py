
from ipsum.service.crud_service import CRUDService
from ipsum.tests.resources.data.dao.fake_crud_dao import FakeCRUDDAO
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.tests.resources.service.fake_crud_validator import FakeCRUDValidator

class FakeCRUDService(CRUDService):

    NAME = 'fake-crud-services'

    def __init__(self) -> None:
        dao = FakeCRUDDAO()

        validator = FakeCRUDValidator(dao)

        super().__init__(dao, validator)
