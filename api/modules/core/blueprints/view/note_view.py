

from flask import Blueprint
from api.modules.core.blueprints.service.note.note_service import NoteService
from arq.view.crud_view import CRUDView

# TODO Criar testes de integração
# TODO Usar URI por variavel de ambiente
#   Criar teste testando rest do arq_view, crud_view
#   Criar teste generico para testar testes implementados do arq_view, crud_view ao testar note_view e tag_view

# TODO Buscar de forma generica
note_view_name = 'note'
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(CRUDView):

    def __init__(self) -> None:
        super().__init__(
            service=NoteService()
        )

NoteView.register(note_blueprint)