
from mongoengine import Document
from flask import Blueprint, make_response, request, jsonify
from flask_classful import FlaskView, route
from itsdangerous import json
from api.modules.core.blueprints.service.note.note_service import NoteService
from api.utils.view.query_string_parser import QueryStringParser
from api.utils.view.view_encoder import ViewEncoder


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

        model = self._service.insert(body)

        return self._to_response(model)

    @route('<id>', methods=['GET'])
    def find_by_id(self, id):
        return self._to_response(self._service.find_by_id(id))

    @route('<id>', methods=['PUT'])
    def update(self, id):
        body = request.json

        return self._to_response(self._service.update(id, body))


    @route('', methods=['POST', 'GET'])
    def find(self):

        if request.method == 'POST':
            query_body = request.json

            parsed_query_body = QueryStringParser().parse_dict(query_body)

            return self._to_response(self._service.find(query_filter=parsed_query_body))

        request_query_string = request.query_string

        parsed_query_string = QueryStringParser().parse_string(request_query_string)

        return self._to_response(self._service.find(query_filter=parsed_query_string))
        

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

        
        return self._to_response(self._service.paginate(query_filter=parsed_query_body, limit=limit, page=page))

    @route('<id>', methods=['DELETE'])
    def delete(self, id):
        self._service.delete(id)

        return self._to_response()

    def _to_response(self, object=None):
        answer = ViewEncoder().default(object)

        if answer is None:
            answer = ('', 204)

        return make_response(answer)
   
NoteView.register(note_blueprint)