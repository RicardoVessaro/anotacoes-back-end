
from mongoengine import Document
from bson import ObjectId
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE, PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.util import object_util
from ipsum.util.data.query_filter_builder import QueryFilterBuilder

class DAO:

    def __init__(self, model:Document) -> None:
        self._model = model

    @property
    def model(self):
        return self._model

    def insert(self, model_data, **kwargs) -> str:
        model_data.save(**kwargs)

        return model_data

    def delete(self, id, validate_if_none=False):
        model = self.find_by_id(id)

        if model is None:
            if validate_if_none:
                exception_message = OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(id)
                raise IpsumException(exception_message, status_code=404)

            else:
                return None

        deleted_id = model.id

        model.delete()

        return str(deleted_id)

        
    def find_by_id(self, id):
        _id = id

        if type(id) is str:
            _id = ObjectId(id)

        return self._model.objects(id=_id).first()

    def find(self, **query_filter):

        if object_util.is_none_or_empty(query_filter, verify_iterable_values=False):
            return self._model.objects()

        else:    
            built_query_filter = QueryFilterBuilder().build(query_filter)
        
            return self._model.objects(**built_query_filter)

    def paginate(self, page=1, limit=5, **query_filter) -> dict:
        results = self.find(**query_filter)

        return self._build_pagination(results, page, limit)

    def _build_pagination(self, results, page, limit):

        total = len(results)

        if total == 0:
            return {
                'items': [],
                'page': 0,
                'limit': 0,
                'total': total,
                'pages': 0,
                'has_prev': False,
                'has_next': False,
                'has_result': False
            }

        mod = total % limit
        int_div = total // limit

        pages = int_div
        if mod > 0:
            pages += 1

        if page > pages:
            raise IpsumException(PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(page, pages))
        
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
            'has_next': has_next,
            'has_result': True
        }
