
import re
from ipsum.util.object_util import is_none_or_empty

class DAOQuery:

    SORT = '_sort'
    FIELDS = '_fields'

    AND = 'and'
    OR = 'or'
    EQ = 'eq'
    OP = '_op'

    LEFT_SQUARE_BRACKET = '['
    RIGHT_SQUARE_BRACKET = ']'
    LOGICAL_SEPARATOR = ':'
    BRACKET_REGEX = r'[\[\]]'

    def __init__(self) -> None:
        pass

    def build(self, _fields=None, _sort=None, **kwargs) -> dict:

        query_dict = dict(kwargs.items())

        query_fields = self._get_query_fields(_fields)

        query_sort = self._get_sort_fields(_sort)

        query_filter = self._build_query_filter(query_dict)
            
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

    def _build_query_filter(self, query_dict):
        if is_none_or_empty(query_dict):
            return None

        query_operator = self.AND

        if self.OP in query_dict:
            if query_dict[self.OP] == self.OR:
                query_operator = self.OR

            query_dict.pop(self.OP)

        dao_query = {query_operator: {}}

        for field_operation, value in query_dict.items():

            field_operator = self.AND
            expression = self.EQ
            field = field_operation

            if self.LEFT_SQUARE_BRACKET in field_operation and self.RIGHT_SQUARE_BRACKET in field_operation:
                re_split = re.split(self.BRACKET_REGEX, field_operation)
                
                field = re_split[0]

                expression_str = re_split[1].split()
                expression = ''
                for s in expression_str:
                    expression += s

                if self.LOGICAL_SEPARATOR in expression:
                    logical_split = expression.split(self.LOGICAL_SEPARATOR)

                    field_operator = logical_split[0]
                    expression = logical_split[1]

            dao_query[query_operator][field] = {field_operator : { expression: value } }

        return dao_query
