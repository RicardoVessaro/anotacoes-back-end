
from ipsum.util.object_util import is_none_or_empty


class QueryFilter:

    _IN_LIST_SUFIX = '__in'

    SORT = '_sort'

    def __init__(self) -> None:
        pass

    def build(self, _fields=None, _sort=None, **kwargs) -> dict:

        query_dict = dict(kwargs.items())

        query_fields = self._set_fields(_fields)

        query_sort = self._set_sort(_sort)

        query_filter = self._set_list_filters(query_dict)
            
        return query_filter, query_fields, query_sort

    def _set_fields(self, query_fields):
        # TODO ver _set_sort

        return None

    def _set_sort(self, query_sort):
        if not is_none_or_empty(query_sort):

            if type(query_sort) is str:
                return (query_sort,)

            return tuple(query_sort)

        return None

    def _set_list_filters(self, query_dict:dict):
        query_filter_param = {}

        for field, value in query_dict.items():
            query_filter_field = field

            if type(value) is list or type(value) is tuple:
                query_filter_field = field + self._IN_LIST_SUFIX

            query_filter_param[query_filter_field] = value

        return query_filter_param
