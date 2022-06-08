from flask_classful import FlaskView, route
from flask import make_response, request
from ipsum.util.view.query_string_parser import QueryStringParser

from ipsum.service.service import Service
from ipsum.util.view.view_encoder import ViewEncoder

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'

QUERY_LIMIT = 'limit'
QUERY_PAGE = 'page'

STATUS_NO_CONTENT = 204

class IpsumView(FlaskView):

    def __init__(self, service: Service) -> None:
        super().__init__()

        self._service = service

    @property
    def service(self):
        return self._service

    @route('<id>', methods=[GET])
    def find_by_id(self, id, **kwargs):
        return self._to_response(self._service.find_by_id(id))

    @route('', methods=[GET])
    def find(self, **kwargs):

        request_query_string = request.query_string

        parsed_query_string = QueryStringParser().parse_string(request_query_string)

        return self._to_response(self._service.find(**parsed_query_string))

    @route('paginate', methods=[POST])
    def paginate(self, **kwargs):
        query_body = request.json
        parsed_query_body = QueryStringParser().parse_dict(query_body)

        limit = 5
        if QUERY_LIMIT in parsed_query_body:
            limit = parsed_query_body.pop(QUERY_LIMIT)

        page = 1
        if QUERY_PAGE in parsed_query_body:
            page = parsed_query_body.pop(QUERY_PAGE)

        
        return self._to_response(self._service.paginate(limit=limit, page=page, **parsed_query_body))

    def _to_response(self, object=None):
        answer = ViewEncoder().default(object)

        if answer is None:
            answer = ('', STATUS_NO_CONTENT)

        return make_response(answer)