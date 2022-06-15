
from flask import request
from ipsum.util.view.query_string_parser import QueryStringParser
from ipsum.view.ipsum_view import GET, PATCH, POST, QUERY_LIMIT, QUERY_OFFSET
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

    @route('', methods=[POST])
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

    @route('', methods=[GET])
    def find(self, **kwargs):
        parent_id = request.collection_tree.parent.id

        parsed_query_string, limit, offset = self._build_paginate_params()

        return self._to_response(
            self._service.paginate(parent_id, offset=offset, limit=limit, **parsed_query_string)
        )
