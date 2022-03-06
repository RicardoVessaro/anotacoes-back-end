
from arq.service.arq_service import ArqService

class ArqCRUDService(ArqService):

    def __init__(self, dao, validator, non_editable_fields=[]) -> None:
        super().__init__(dao, validator, non_editable_fields)

    def insert(self, body: dict):
        self._validator.validate_insert(body)
        return self._dao.insert(body)

    def update(self, id, body: dict):
        body = self._remove_non_editable_fields(body)

        self._validator.validate_update(id, body)

        return self._dao.update(id, body)

    def delete(self, id):
        self._validator.validate_delete(id)

        return self._dao.delete(id)

    def _remove_non_editable_fields(self, body: dict):
        editable_body = {}

        for field, value in body.items():
            if field not in self._non_editable_fields:
                editable_body[field] = value

        return editable_body
