
class QueryFilter:

    _IN_LIST_SUFIX = '__in'

    def __init__(self) -> None:
        pass

    def build(self, **kwargs) -> dict:
        query_filter_param = {}

        for field, value in kwargs.items():
            query_filter_field = field

            if type(value) is list or type(value) is tuple:
                query_filter_field = field + self._IN_LIST_SUFIX

            query_filter_param[query_filter_field] = value
            
        return query_filter_param
