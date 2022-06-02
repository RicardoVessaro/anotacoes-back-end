
from flask import Blueprint
from api.modules.core.blueprints.general.module_constants import REST_API_V1_BASE_URL
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.view.detail_crud_view import DetailCRUDView
from api.modules.core.blueprints.service.note.link.link_service import LinkService
from api.modules.core.blueprints.data.model.link import Link

link_view_name = LinkService.NAME
link_blueprint = Blueprint(link_view_name, __name__)

class LinkView(DetailCRUDView):

    route_prefix = f'{REST_API_V1_BASE_URL}{NoteService.NAME}/<{Link.parent_field}>/'

    def __init__(self) -> None:
        super().__init__(service=LinkService())

LinkView.register(link_blueprint)