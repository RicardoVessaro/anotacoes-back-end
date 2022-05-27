
from flask import request
from flask_classful import route
from arq.service.crud_service import CRUDService
from arq.view.arq_view import DELETE, POST, PUT, ArqView


class CRUDView(ArqView):

    def __init__(self, service: CRUDService) -> None:
        super().__init__(
            service=service
        )

    @route('/', methods=[POST])
    def insert(self, **kwargs):
        body = request.json

        model = self._service.insert(body)

        return self._to_response(model)


    @route('<id>', methods=[PUT])
    def update(self, id, **kwargs):
        body = request.json

        update_response = self._service.update(id, body)
        
        return self._to_response(update_response)

    @route('<id>', methods=[DELETE])
    def delete(self, id, **kwargs):
        self._service.delete(id)

        return self._to_response()

    