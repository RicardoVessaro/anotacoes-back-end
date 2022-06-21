
from flask import Blueprint
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from api.annotation.service.note.note_service import NoteService
from ipsum.view.detail_crud_view import DetailCRUDView
from api.annotation.service.note.link.link_service import LinkService
from api.annotation.data.model.link import Link

link_view_name = LinkService.NAME
link_blueprint = Blueprint(link_view_name, __name__)

class LinkView(DetailCRUDView):

    route_prefix = f'{REST_API_V1_BASE_URL}{NoteService.NAME}/<{Link.parent_field}>/'

    route_base = link_view_name

    def __init__(self) -> None:
        
        super().__init__(
            service=LinkService()
        )

LinkView.register(link_blueprint)
