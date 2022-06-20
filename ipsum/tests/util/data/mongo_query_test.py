
from mongoengine.queryset.visitor import Q, QCombination
from pytest import raises
from ipsum.exception.exception_message import MONGOQUERY_CANT_HANDLE_AND_OR_OPERATORS_FOR_THE_SAME_FIELD
from ipsum.exception.ipsum_exception import IpsumException

from ipsum.util.data.mongo_query import MongoQuery

class TestMongoQuery:

    def test_raise_excecption_when_two_operators_to_same_field(self):
        dao_query = {
            'or': {
                    'code': {
                        'or': {'gte': 3, 'lte': 7},
                        'and': {'eq': 5}
                    },
                }
            }

        with raises(IpsumException, match=MONGOQUERY_CANT_HANDLE_AND_OR_OPERATORS_FOR_THE_SAME_FIELD.format(MongoQuery, MongoQuery.AND, MongoQuery.OR)):
            mongo_query = MongoQuery().build(dao_query)

    def test_with_two_operations_to_same_field(self):
        dao_query = {'and': {
                'code': {'and': {'gte': 3, 'lte': 7}},
            }
        }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = Q(code__gte=3) & Q(code__lte=7)

        assert expected_query == mongo_query

    def test_with_two_operations_to_same_field_using_or(self):
        dao_query = {'and': {
                'code': {'or': {'gte': 3, 'lte': 7}},
            }
        }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = Q(code__gte=3) | Q(code__lte=7)

        assert expected_query == mongo_query


    def test_with_empty_values(self):

        assert MongoQuery().build(None) is None

        dao_query = {
            'or': {}
        }

        assert MongoQuery().build(dao_query) is None

        dao_query = {
            'or': None
        }

        assert MongoQuery().build(dao_query) is None

        dao_query = {
            'or': {
                'code': {}
            }
        }

        assert MongoQuery().build(dao_query) is None

        dao_query = {
            'or': {
                'code': None
            }
        }

        assert MongoQuery().build(dao_query) is None

        dao_query = {
            'or': {
                'code': {'or': {} }
            }
        }

        assert MongoQuery().build(dao_query) is None

        dao_query = {
            'or': {
                'code': {'or': None }
            }
        }

        assert MongoQuery().build(dao_query) is None

        dao_query = {
            'or': {
                'code': {'or': {'eq': None} }
            }
        }

        assert Q(code=None) == MongoQuery().build(dao_query)

    def test_with_item_code_none_and_name(self):
        dao_query = {
            'and': {
                    'code': {'or': {'eq': None}},
                    'name': {'and': {'eq': 'Test'} }
                }
            }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = Q(code=None) & Q(name='Test')

        assert expected_query == mongo_query

    def test_with_single_item_code_or(self):
        dao_query = {
            'and': {
                    'code': {'or': {'eq': 1}}
                }
            }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = Q(code=1)

        assert expected_query == mongo_query

    def test_with_single_item_code_and(self):
        dao_query = {
            'and': {
                    'code': {'and': {'eq': 1}}
                }
            }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = Q(code=1)

        assert expected_query == mongo_query

    def test_with_or_in(self):
        dao_query = {
            'and': {
                    'tags': {'or': {'in': ['A']}}
                }
            }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = Q(tags__in=['A'])

        assert expected_query == mongo_query

    def test_or_complex_query(self):
        dao_query = {
            'or': {
                'code': {'or': {'eq': [1, 2]}}, 
                'priority': {'and': {'lte': 1}}, 
                'tags': {'and': {'in': ['A']}}, 
                'boolean': {'and': {'eq': True}},
                'name': {'or': {'ne': ['Test', 'sesT']}},
                'series': {'or': {'aeq': [[1, 2], [8, 9]]}}
            }
        }


        mongo_query = MongoQuery().build(dao_query)

        expected_query = (Q(code=1) | Q(code=2) ) | (Q(name__ne='Test') | Q(name__ne='sesT')) | (Q(series__all=[1,2]) | Q(series__all=[8,9])) | Q(priority__lte=1)  | Q(tags__in=['A'])  | Q(boolean=True)

        assert expected_query == mongo_query

    def test_and_complex_query(self):
        dao_query = {
            'and': {
                'code': {'or': {'eq': [1, 2]}}, 
                'priority': {'and': {'lte': 1}}, 
                'tags': {'and': {'in': ['A']}}, 
                'boolean': {'and': {'eq': True}},
                'name': {'or': {'ne': ['Test', 'sesT']}},
                'series': {'or': {'aeq': [[1, 2], [8, 9]]}}
            }
        }

        mongo_query = MongoQuery().build(dao_query)

        expected_query = (Q(code=1) | Q(code=2)) & (Q(name__ne='Test') | Q(name__ne='sesT')) & (Q(series__all=[1,2]) | Q(series__all=[8,9])) & Q(priority__lte=1) & Q(tags__in=['A']) & Q(boolean=True)

        assert expected_query == mongo_query


    