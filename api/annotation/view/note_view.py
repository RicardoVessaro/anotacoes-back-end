
from flask import Blueprint
from api.annotation.service.note.note_service import NoteService
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from ipsum.view.crud_view import CRUDView

note_view_name = NoteService.NAME
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(CRUDView):

    route_prefix = REST_API_V1_BASE_URL

    route_base = note_view_name

    def __init__(self) -> None:
        super().__init__(
            service=NoteService()
        )

NoteView.register(note_blueprint)