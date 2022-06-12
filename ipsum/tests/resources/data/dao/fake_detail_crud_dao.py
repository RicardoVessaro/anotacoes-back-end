
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.tests.resources.data.model.detail_test_model import DetailTestModel

class FakeDetailCRUDDAO(DetailCRUDDAO):

    def __init__(self) -> None:
        model = DetailTestModel

        cascade=None
        
        dependent=None

        super().__init__(model, cascade, dependent)
