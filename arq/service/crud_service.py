
from arq.service.service import Service

class CRUDService(Service):

    def __init__(self, dao, validator, non_editable_fields=[]) -> None:
        super().__init__(dao)
        self._validator = validator
        self._non_editable_fields = non_editable_fields

    def insert(self, body, **kwargs):
        self._validator.validate_insert(body)
        return self._dao.insert(body, **kwargs)

    def update(self, id, body, **kwargs):
        is_dict = type(body) == dict

        if is_dict:
            body = self._remove_non_editable_fields_from_dict(body)

        else :
            body = self._remove_non_editable_fields_from_model(id, body)

        self._validator.validate_update(id, body)

        return self._dao.update(id, body, **kwargs)

    def delete(self, id):
        self._validator.validate_delete(id)

        return self._dao.delete(id)

    def _remove_non_editable_fields_from_dict(self, body: dict):
        editable_body = {}

        for field, value in body.items():
            if field not in self._non_editable_fields:
                editable_body[field] = value

        return editable_body

    def _remove_non_editable_fields_from_model(self, id, body):
        model = self.find_by_id(id)

        for field, value in body.to_mongo().items():
            if field in self._non_editable_fields:
                body[field] = model[field]

        return body
