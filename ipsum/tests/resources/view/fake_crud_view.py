
from ipsum.view.crud_view import CRUDView
from ipsum.tests.resources.service.fake_crud_service import FakeCRUDService

class FakeCRUDView(CRUDView):

    route_prefix = 'ipsum/api/v1/tests/'

    route_base = FakeCRUDService.NAME

    def __init__(self) -> None:
        service = FakeCRUDService()
        
        super().__init__(service)
