
from flask import Blueprint, request, jsonify
from flask_classful import FlaskView, route
from itsdangerous import json
from api.modules.core.blueprints.service.note.note_service import NoteService
from api.utils.view.query_string_parser import QueryStringParser


# TODO Ver testes de integração

# TODO Buscar de forma generica
note_view_name = 'materia'
note_blueprint = Blueprint(note_view_name, __name__)

class NoteView(FlaskView):

    def __init__(self) -> None:
        super().__init__()

        self._service = NoteService()

    @route('/', methods=['POST'])
    def insert(self):
        body = request.json

        return jsonify(self._service.insert(body))

    @route('<id>', methods=['GET'])
    def find_by_id(self, id):
        return jsonify(self._service.find_by_id(id))

    # TODO conferir o que deve ser retornado em um update
    @route('<id>', methods=['PUT'])
    def update(self, id):
        body = request.json

        return jsonify(self._service.update(id, body))


    @route('', methods=['POST', 'GET'])
    def find(self):

        if request.method == 'POST':
            query_body = request.json

            parsed_query_body = QueryStringParser().parse_dict(query_body)

            return jsonify(self._service.find(query_filter=parsed_query_body))

        request_query_string = request.query_string

        parsed_query_string = QueryStringParser().parse_string(request_query_string)

        return jsonify(self._service.find(query_filter=parsed_query_string))
        

    @route('paginate', methods=['POST'])
    def paginate(self):
        QUERY_LIMIT = 'limit'
        QUERY_PAGE = 'page'

        query_body = request.json
        parsed_query_body = QueryStringParser().parse_dict(query_body)

        limit = 5
        if QUERY_LIMIT in parsed_query_body:
            limit = parsed_query_body.pop(QUERY_LIMIT)

        page = 1
        if QUERY_PAGE in parsed_query_body:
            page = parsed_query_body.pop(QUERY_PAGE)

        return jsonify(self._service.paginate(query_filter=parsed_query_body, limit=limit, page=page))


    # TODO conferir o que deve ser retornado em um delete
    @route('<id>', methods=['DELETE'])
    def delete(self, id):
        return jsonify(self._service.delete(id))
   


NoteView.register(note_blueprint)