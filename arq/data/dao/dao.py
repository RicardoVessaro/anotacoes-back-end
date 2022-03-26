
from mongoengine import Document
from bson import ObjectId
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from arq.util import object_util
from arq.util.data.query_filter_builder import QueryFilterBuilder

class Dao:

    def __init__(self, model:Document) -> None:
        self._model = model

    def insert(self, model_data) -> str:
        model_data.save()

        return model_data

    def delete(self, id):
        model = self.find_by_id(id)

        if model is None:
            return None

        deleted_id = model.id

        model.delete()

        return str(deleted_id)

        
    def find_by_id(self, id):
        _id = id

        if type(id) is str:
            _id = ObjectId(id)

        return self._model.objects(id=_id).first()

    def find(self, query_filter={}):

        if object_util.is_none_or_empty(query_filter):
            return self._model.objects()

        else:    
            built_query_filter = QueryFilterBuilder().build(query_filter)
        
            return self._model.objects(**built_query_filter)

    def paginate(self, query_filter={}, page=1, limit=5) -> dict:
        results = self.find(query_filter)

        total = len(results)
        mod = total % limit
        int_div = total // limit

        pages = int_div
        if mod > 0:
            pages += 1

        if page > pages:
            raise ArqException(PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(page, pages))
        
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
