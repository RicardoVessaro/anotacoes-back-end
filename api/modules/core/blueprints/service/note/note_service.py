
import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from api.modules.core.blueprints.service.note.note_validator import NoteValidator

class NoteService:

    def __init__(self) -> None:
        self._dao = NoteDAO()
        self._validator = NoteValidator()
        self._non_editable_fields = ['created_in']

    def insert(self, body: dict):
        body['created_in'] = datetime.datetime.today()
        
        self._validator.validate_insert(body)
        return self._dao.insert(body)

    def find_by_id(self, id):
        return self._dao.find_by_id(id)

    def update(self, id, body: dict):
        body = self._remove_non_editable_fields(body)

        self._validator.validate_update(id, body)

        return self._dao.update(id, body)

    def find(self, query_filter={}):
        return self._dao.find(query_filter)

    def delete(self, id):
        self._validator.validate_delete(id)

        return self._dao.delete(id)

    def paginate(self, query_filter={}, page=1, limit=5):
        return self._dao.paginate(query_filter=query_filter, page=page, limit=limit)
        
    def _remove_non_editable_fields(self, body: dict):
        editable_body = {}

        for field, value in body.items():
            if field not in self._non_editable_fields:
                editable_body[field] = value

        return editable_body
