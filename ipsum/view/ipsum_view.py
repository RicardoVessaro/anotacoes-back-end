
from flask_classful import FlaskView, route
from flask import make_response, request
from ipsum.util.data.dao_query import DAOQuery
from ipsum.util.view import hateoas_builder
from ipsum.util.view.query_string_parser import QueryStringParser

from ipsum.service.service import Service
from ipsum.util.view.view_encoder import ViewEncoder

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'

QUERY_LIMIT = '_limit'
QUERY_OFFSET = '_offset'
QUERY_SORT = DAOQuery.SORT

STATUS_NO_CONTENT = 204

# TODO rename id enum 'ID'
class IpsumView(FlaskView):

    PAGINATE_REQUEST = 'find'

    FIND_BY_ID_REQUEST = 'find_by_id'

    def __init__(self, service: Service) -> None:
        super().__init__()

        self._service = service

    def after_request(self, name, response, *args, **kwargs):

        hateoas = hateoas_builder.HATEOASBuilder(
            response_data=response.get_data(),
            view=self, 
            host_url=request.host_url, 
            view_args=request.view_args,
            request_name=name,
            query_string=request.query_string
        )

        hateoas_response = hateoas.build()

        response.set_data(hateoas_response)

        return response

    @property
    def service(self):
        return self._service

    @route('<id>', methods=[GET])
    def find_by_id(self, id, **kwargs):
        return self._to_response(self._service.find_by_id(id))

    @route('', methods=[GET])
    def find(self, **kwargs):
        
        parsed_query_string, limit, offset = self._get_query_params()

        return self._to_response(self._service.paginate(offset=offset, limit=limit, **parsed_query_string))

    def _get_query_params(self):
        parsed_query_string = self._get_parsed_query_string()

        limit, offset = self._get_paginate_params(parsed_query_string)

        return parsed_query_string, limit, offset

    def _get_paginate_params(self, parsed_query_string):
        limit = 5
        if QUERY_LIMIT in parsed_query_string:
            limit = parsed_query_string.pop(QUERY_LIMIT)

        offset = 0
        if QUERY_OFFSET in parsed_query_string:
            offset = parsed_query_string.pop(QUERY_OFFSET)

        return limit, offset

    def _get_parsed_query_string(self):
        return QueryStringParser().parse_string(request.query_string)

    def _to_response(self, object=None):
        answer = ViewEncoder().default(object)

        if answer is None:
            answer = ('', STATUS_NO_CONTENT)

        return make_response(answer)