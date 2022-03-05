
from api.modules.core.blueprints.data.model.note import Note
from api.utils.data.query_filter_builder import QueryFilterBuilder
from bson import ObjectId
from api.utils import object_util

class NoteDAO:

    OBJECT_NOT_FOUND_EXCEPTION_MESSAGE = "Object with ID {0} not found."
    PAGE_NOT_FOUND_EXCEPTION_MESSAGE = "Page {0} not found. The max number os pages is {1}."

    def __init__(self) -> None:
        self._model = Note

    def insert(self, model_data: dict) -> str:
        model = self._model(**model_data)
        model.save()

        return model

    def find_by_id(self, id):
        _id = id

        if type(id) is str:
            _id = ObjectId(id)

        return self._model.objects(id=_id).first()

    def update(self, id, model_date: dict):
        model = self.find_by_id(id)

        for key, value in model_date.items():
            model[key] = value

        return model.save()

    def find(self, query_filter={}):

        if object_util.is_none_or_empty(query_filter):
            return self._model.objects()

        else:    
            built_query_filter = QueryFilterBuilder().build(query_filter)
        
            return self._model.objects(**built_query_filter)
        
    def delete(self, id):
        model = self.find_by_id(id)

        if model is None:
            exception_message = self.OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(id)
            raise Exception(exception_message)

        deleted_id = model.id

        model.delete()

        return str(deleted_id)

    def paginate(self, query_filter={}, page=1, limit=5) -> dict:
        results = self.find(query_filter)

        total = len(results)
        mod = total % limit
        int_div = total // limit

        pages = int_div
        if mod > 0:
            pages += 1

        if page > pages:
            raise Exception(self.PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(page, pages))
        
        start = page * limit - limit
        end = start + limit

        results_slice = results[start:end]

        items = []
        for result in results_slice:
            items.append(result)

        
        has_prev = page != 1
        has_next = page != pages

        return {
            'items': items,
            'page': page,
            'limit': limit,
            'total': total,
            'pages': pages,
            'has_prev': has_prev,
            'has_next': has_next
        }
