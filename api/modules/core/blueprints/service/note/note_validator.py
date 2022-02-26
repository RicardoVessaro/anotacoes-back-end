from api.utils.object_util import is_none_or_empty

# TODO mudar exceptions para exceptions proprias
class NoteValidator:

    REQUIRED_FIELD_EXCEPTION_MESSAGE = "The field '{0}' is required."

    def __init__(self) -> None:
        self.required_fields = ['pinned', 'text', 'created_in']

    def validate_insert(self, body: dict):
       self._validate_required_fields_on_insert(body)

    def validate_update(self, id, body: dict):
        self._validate_required_fields_on_update(body)

    def validate_delete(self, id):
        pass

    def _validate_required_fields_on_insert(self, body: dict):

        for required_field in self.required_fields:
            if required_field not in body.keys() or is_none_or_empty(body[required_field]):
                self._raise_required_field_exception(required_field)

    def _validate_required_fields_on_update(self, body: dict):
        for field, value in body.items():

            if field in self.required_fields and is_none_or_empty(value):
                self._raise_required_field_exception(field)

    def _raise_required_field_exception(self, required_field: str):
        raise Exception(self.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field))
        