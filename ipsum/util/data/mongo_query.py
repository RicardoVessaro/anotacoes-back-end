
from mongoengine.queryset.visitor import Q, QCombination

from ipsum.util.object_util import is_iterable, is_none_or_empty

class MongoQuery:

    AND = 'and'
    OR = 'or'

    EQ = 'eq'
    IN = 'in'
    NIN = 'nin'
    AEQ = 'aeq'

    # MongoDB 'AEQ' operator doesn't exists so we use 'ALL'
    ALL = 'all'

    LIST_OPERATORS = [
        IN, 
        NIN,
        AEQ
    ]

    def __init__(self) -> None:
        pass

    def build(self, dao_query):

        if is_none_or_empty(dao_query, verify_iterable_values=False) or dao_query == {}:
            return None

        operator = self.AND
        if self.OR in dao_query:
            operator = self.OR

        filter = dao_query[operator]

        if is_none_or_empty(filter, verify_iterable_values=False) or filter == {}:
            return None

        nested_expressions, single_expressions = self._separate_expressions(filter)

        q_operator = self._get_q_operator(operator)

        q_combination_nested_expressions = self._combine_expression(nested_expressions, q_operator)

        if is_none_or_empty(single_expressions):

            if not is_none_or_empty(q_combination_nested_expressions):
                return q_combination_nested_expressions

            return None

        q_combination_single_expressions = self._combine_expression(single_expressions, q_operator)

        if is_none_or_empty(q_combination_nested_expressions):
            return q_combination_single_expressions

        return QCombination(q_operator, [q_combination_nested_expressions, q_combination_single_expressions])

    def _combine_expression(self, expressions, q_operator):
        q_combination = None
        
        for expression in expressions:

            if q_combination is None:
                q_combination = expression

            else:
                q_combination = QCombination(q_operator, [q_combination, expression])

        return q_combination

    def _get_q_operator(self, operator):
        q_operator = QCombination.AND
        if operator == self.OR:
            q_operator = QCombination.OR
        return q_operator

    def _separate_expressions(self, filter):
        nested_expressions = []
        single_expressions = []

        for field, expression in filter.items():
            if is_none_or_empty(expression, verify_iterable_values=False) or expression == {}:
                continue

            expression_operator = self._get_expression_operator(expression)

            operation = expression[expression_operator]

            if is_none_or_empty(operation, verify_iterable_values=False) or operation == {}:
                continue

            for comparison_operator, value in operation.items():
                field_expression = self._get_field_expression(field, comparison_operator)
                    
                q_expression = Q(**{field_expression: value})

                if is_iterable(value) and not type(value) is str:
                    is_list_operator = comparison_operator in self.LIST_OPERATORS

                    is_list_of_lists = is_iterable(value[0]) and not type(value[0]) is str 

                    if not is_list_operator or is_list_operator and is_list_of_lists:
                        q_exp = []

                        for v in value:
                            q_exp.append(Q(**{field_expression: v}))


                        q_expression = QCombination(QCombination.OR, q_exp)

                if expression_operator == self.OR:
                    nested_expressions.append(q_expression)
                
                else:
                    single_expressions.append(q_expression)

        return nested_expressions,single_expressions

    def _get_field_expression(self, field, comparison_operator):
        field_expression = field
        if comparison_operator != self.EQ:
            field_expression = f'{field}__{comparison_operator}'
                    
            if comparison_operator == self.AEQ:
                field_expression = f'{field}__{self.ALL}'
        return field_expression

    def _get_expression_operator(self, expression):
        expression_operator = self.AND

        if self.OR in expression:
            expression_operator = self.OR
        return expression_operator
