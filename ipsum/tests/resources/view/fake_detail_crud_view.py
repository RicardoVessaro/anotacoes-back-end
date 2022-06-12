
from ipsum.tests.resources.data.model.detail_test_model import DetailTestModel
from ipsum.tests.resources.service.fake_crud_service import FakeCRUDService
from ipsum.view.detail_crud_view import DetailCRUDView
from ipsum.tests.resources.service.fake_detail_crud_service import FakeDetailCRUDService

class FakeDetailCRUDView(DetailCRUDView):

    route_prefix = f'ipsum/api/v1/tests/{FakeCRUDService.NAME}/<{DetailTestModel.parent_field}>/'

    route_base = FakeDetailCRUDService.NAME

    def __init__(self) -> None:
        service = FakeDetailCRUDService()

        super().__init__(service)
