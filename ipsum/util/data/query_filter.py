
from ipsum.util.object_util import is_none_or_empty


class QueryFilter:

    _IN_LIST_SUFIX = '__in'

    SORT = '_sort'

    FIELDS = '_fields'

    def __init__(self) -> None:
        pass

    def build(self, _fields=None, _sort=None, **kwargs) -> dict:

        query_dict = dict(kwargs.items())

        query_fields = self._get_query_fields(_fields)

        query_sort = self._get_sort_fields(_sort)

        query_filter = self._set_list_filters(query_dict)
            
        return query_filter, query_fields, query_sort

    def _get_query_fields(self, _fields):
        if is_none_or_empty(_fields):
            return None
            
        if type(_fields) is str:
            return {'$project': {_fields: 1}}

        fields = {}
        for field in _fields:
            fields[field] = 1

        return {'$project': fields}


    def _get_sort_fields(self, query_values):
        if not is_none_or_empty(query_values):

            if type(query_values) is str:
                return (query_values,)

            return tuple(query_values)

        return None

    def _set_list_filters(self, query_dict:dict):
        query_filter_param = {}

        for field, value in query_dict.items():
            query_filter_field = field

            if type(value) is list or type(value) is tuple:
                query_filter_field = field + self._IN_LIST_SUFIX

            query_filter_param[query_filter_field] = value

        return query_filter_param
