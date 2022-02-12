
from flask import Blueprint, request, jsonify
from flask_classful import FlaskView, route
from api.modules.core.blueprints.service.note.note_service import NoteService

note_view_name = 'materia' # Buscar de forma generica
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(FlaskView):

    def __init__(self) -> None:
        super().__init__()

        self._service = NoteService()

    @route('/', methods=['POST'])
    def insert(self):
        body = request.json

        return jsonify(self._service.insert(body))

    @route('', methods=['GET'])
    def find(self):
        return "find"

    @route('<id>', methods=['GET'])
    def find_by_id(self, id):
        return "find_by_id"

    @route('<id>', methods=['DELETE'])
    def delete(self, id):
        return "delete"
   


NoteView.register(note_blueprint)