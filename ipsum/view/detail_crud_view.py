
from flask import request
from ipsum.util.view.query_string_parser import QueryStringParser
from ipsum.view.ipsum_view import GET, PATCH, POST, QUERY_LIMIT, QUERY_PAGE
from ipsum.view.crud_view import CRUDView
from flask_classful import route

from ipsum.service.detail_crud_service import DetailCRUDService

class DetailCRUDView(CRUDView):

    def __init__(self, service: DetailCRUDService) -> None:
        super().__init__(service=service)

    def before_request(self, name, *args, **kwargs):
        collection_tree = self._service.build_collection_tree_ids(kwargs)
        self._service.validate_collection_tree(collection_tree)

        request.collection_tree = collection_tree

    @route('/', methods=[POST])
    def insert(self, **kwargs):
        collection_tree = request.collection_tree
        parent = collection_tree.parent
        
        request.json[parent.field] = parent.id

        return super().insert(**kwargs)
    
    @route('<id>', methods=[PATCH])
    def update(self, id, **kwargs):
        collection_tree = request.collection_tree
        parent = collection_tree.parent
        
        if parent.field not in request.json:
            request.json[parent.field] = parent.id

        return super().update(id, **kwargs)

    @route('', methods=[POST, GET])
    def find(self, **kwargs):
        parent_id = request.collection_tree.parent.id

        if request.method == POST:
            query_body = request.json

            parsed_query_body = QueryStringParser().parse_dict(query_body)

            return self._to_response(
                self._service.find(parent_id, **parsed_query_body)
            )

        request_query_string = request.query_string

        parsed_query_string = QueryStringParser().parse_string(request_query_string)

        return self._to_response(
            self._service.find(parent_id, **parsed_query_string)
        )
        
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

        parent_id = request.collection_tree.parent.id

        return self._to_response(
            self._service.paginate(parent_id, page=page, limit=limit, **parsed_query_body)
        )
