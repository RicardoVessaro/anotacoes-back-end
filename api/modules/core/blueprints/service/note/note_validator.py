from api.utils.object_util import is_none_or_empty

class NoteValidator:

    REQUIRED_FIELD_EXCEPTION_MESSAGE = "The field '{0}' is required."

    def __init__(self) -> None:
        self.required_fields = ['title', 'pinned', 'pinned', 'created_in']

    def validate_insert(self, body: dict):
       self._validate_required_fields_on_insert(body)

    def _validate_required_fields_on_insert(self, body: dict):

        for required_field in self.required_fields:
            if required_field not in body.keys() or is_none_or_empty(body[required_field]):
                self._raise_required_field_exception(required_field)


    def _raise_required_field_exception(self, required_field: str):
        raise Exception(self.REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field))