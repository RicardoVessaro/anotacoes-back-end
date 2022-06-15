
import json
from flask_classful import FlaskView, route
from flask import make_response, request
from ipsum.util.view.hateoas_builder import HATEOASBuilder
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

    def after_request(self, name, response, *args, **kwargs):

        hateoas_builder = HATEOASBuilder(
            response_data=response.get_data(),
            view=self, 
            host_url=request.host_url, 
            view_args=request.view_args,
            request_name=name
        )

        hateoas_response = hateoas_builder.build()

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

        parsed_query_string = self._get_parsed_query_string()

        return self._to_response(self._service.find(**parsed_query_string))

    @route('paginate', methods=[GET])
    def paginate(self, **kwargs):
        
        parsed_query_string, limit, page = self._build_paginate_params()

        return self._to_response(self._service.paginate(limit=limit, page=page, **parsed_query_string))

    def _build_paginate_params(self):
        parsed_query_string = self._get_parsed_query_string()

        limit, page = self._get_paginate_params(parsed_query_string)
        return parsed_query_string,limit,page

    def _get_paginate_params(self, parsed_query_string):
        limit = 5
        if QUERY_LIMIT in parsed_query_string:
            limit = parsed_query_string.pop(QUERY_LIMIT)

        page = 1
        if QUERY_PAGE in parsed_query_string:
            page = parsed_query_string.pop(QUERY_PAGE)
        return limit,page

    def _get_parsed_query_string(self):
        return QueryStringParser().parse_string(request.query_string)

    def _to_response(self, object=None):
        answer = ViewEncoder().default(object)

        if answer is None:
            answer = ('', STATUS_NO_CONTENT)

        return make_response(answer)