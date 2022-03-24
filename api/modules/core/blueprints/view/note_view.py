

from flask import Blueprint
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.view.arq_crud_view import ArqCRUDView

# TODO Ver testes de integração

# TODO Buscar de forma generica
note_view_name = 'note'
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(ArqCRUDView):

    def __init__(self) -> None:
        super().__init__(
            service=NoteService()
        )

        self._service = NoteService()

NoteView.register(note_blueprint)