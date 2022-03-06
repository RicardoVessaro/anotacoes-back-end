
from flask import request
from flask_classful import route
from arq.service.arq_crud_service import ArqCRUDService
from arq.view.arq_view import ArqView


class ArqCRUDView(ArqView):

    def __init__(self, service: ArqCRUDService) -> None:
        super().__init__(
            service=service
        )

    @route('/', methods=['POST'])
    def insert(self):
        body = request.json

        model = self._service.insert(body)

        return self._to_response(model)


    @route('<id>', methods=['PUT'])
    def update(self, id):
        body = request.json

        return self._to_response(self._service.update(id, body))

    @route('<id>', methods=['DELETE'])
    def delete(self, id):
        self._service.delete(id)

        return self._to_response()

    