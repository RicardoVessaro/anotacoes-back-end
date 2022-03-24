from arq.exception.arq_exception import ArqException
from arq.exception.arq_exception_message import REQUIRED_FIELD_EXCEPTION_MESSAGE
from arq.util.object_util import is_none_or_empty

class ArqCRUDValidator:

    def __init__(self, required_fields=[]) -> None:
        self.required_fields = required_fields

    def validate_insert(self, body):
       self._validate_required_fields_on_insert(body)

    def validate_update(self, id, body):
        self._validate_required_fields_on_update(body)

    def validate_delete(self, id):
        pass

    def _validate_required_fields_on_insert(self, body: dict):
        body_dict = body

        if not type(body) is dict:
            body_dict = body.to_mongo()

        for required_field in self.required_fields:
            if required_field not in body_dict.keys() or is_none_or_empty(body_dict[required_field]):
                self._raise_required_field_exception(required_field)

    def _validate_required_fields_on_update(self, body):
        if type(body) is dict:
            self._validate_dict_required_fields_on_updade(body)

        else :
            self._validate_model_required_fields_on_updade(body)

    def _validate_dict_required_fields_on_updade(self, body):
        for field, value in body.items():
            if field in self.required_fields and is_none_or_empty(value):
                self._raise_required_field_exception(field)

    def _validate_model_required_fields_on_updade(self, body):
        for field in self.required_fields:
            if is_none_or_empty(body[field]):
                self._raise_required_field_exception(field)

    def _raise_required_field_exception(self, required_field: str):
        raise ArqException(REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field))
        