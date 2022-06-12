
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel

class FakeCRUDDAO(CRUDDAO):

    def __init__(self) -> None:
        model = IpsumTestModel
        
        cascade = None
        
        dependent = None

        super().__init__(model, cascade, dependent)
