
from flask import request
from flask_classful import route
from ipsum.service.crud_service import CRUDService
from ipsum.view.ipsum_view import DELETE, PATCH, POST, IpsumView


class CRUDView(IpsumView):

    def __init__(self, service: CRUDService) -> None:
        super().__init__(
            service=service
        )

    @route('', methods=[POST])
    def insert(self, **kwargs):
        body = request.json

        model = self._service.insert(body)

        return self._to_response(model)


    @route('<id>', methods=[PATCH])
    def update(self, id, **kwargs):
        body = request.json

        update_response = self._service.update(id, body)
        
        return self._to_response(update_response)

    @route('<id>', methods=[DELETE])
    def delete(self, id, **kwargs):
        self._service.delete(id)

        return self._to_response()

    