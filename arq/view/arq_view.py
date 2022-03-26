from flask_classful import FlaskView, route
from flask import make_response, request
from arq.util.view.query_string_parser import QueryStringParser

from arq.service.service import Service
from arq.util.view.view_encoder import ViewEncoder

class ArqView(FlaskView):

    def __init__(self, service: Service) -> None:
        super().__init__()

        self._service = service

    @route('<id>', methods=['GET'])
    def find_by_id(self, id):
        return self._to_response(self._service.find_by_id(id))

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

    def _to_response(self, object=None):
        answer = ViewEncoder().default(object)

        if answer is None:
            answer = ('', 204)

        return make_response(answer)