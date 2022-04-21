

from flask import Blueprint
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.view.crud_view import CRUDView

note_view_name = 'note'
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(CRUDView):

    def __init__(self) -> None:
        super().__init__(
            service=NoteService()
        )

NoteView.register(note_blueprint)