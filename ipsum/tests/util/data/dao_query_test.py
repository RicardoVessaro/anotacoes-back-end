
from ipsum.util.data.dao_query import DAOQuery


class TestDAOQuery:

    def test_query_filter(self):

        def test_with_two_operations_to_same_field_and_two_operators():
            query_dict = {'code[or:gte]': 3, 'code[or:lte]': 7, 'code':5}

            expected_query_filter = {'and': {
                    'code': {
                        'or': {'gte': 3, 'lte': 7},
                        'and': {'eq': 5}
                    },
                }
            }

            expected_fields = None

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        test_with_two_operations_to_same_field_and_two_operators()

        def test_with_two_operations_to_same_field():
            query_dict = {'code[gte]': 3, 'code[lte]': 7}

            expected_query_filter = {'and': {
                    'code': {'and': {'gte': 3, 'lte': 7}},
                }
            }

            expected_fields = None

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        test_with_two_operations_to_same_field()

        def _test():
            tests = [
                ({'code': 1, 'tags[ nin]': ['A', 'B']}, 
                {
                    'and': {
                        'code': {'and': {'eq': 1}},
                        'tags': {'and': {'nin': ['A', 'B']}}
                    } 
                })
            ]

            for test in tests:
                query_dict = test[0]
                expected_query_filter = test[1]

                assert expected_query_filter == DAOQuery().build(**query_dict)[0]

        _test()

        def _complex_query_filter():
            query_dict = {'_op': 'or', 'code[ or : eq ]': [1, 2], 'priority[lte]': 1, 'tags[and:in]': ['A'], 'boolean': True}

            expected_query_filter = {'or': {
                    'code': {'or': {'eq': [1, 2]}},
                    'priority': {'and': {'lte': 1}},
                    'tags': {'and': {'in': ['A']}},
                    'boolean': {'and': {'eq': True}}
                }
            }

            expected_fields = None

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)
        
        _complex_query_filter()

    def test_query_sort(self):
        
        def _using_list():
            query_dict = {
                DAOQuery.SORT: ['code', '-priority']
            }

            expected_query_filter = None
            expected_fields = None

            expected_sort = ('code', '-priority')

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        _using_list()

        def _using_one_item_list():
            query_dict = {
                DAOQuery.SORT: ['-priority']
            }

            expected_query_filter = None

            expected_fields = None

            expected_sort = ('-priority',)

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        _using_one_item_list()

        def _using_string():
            query_dict = {
                DAOQuery.SORT: '-priority'
            }

            expected_query_filter = None

            expected_fields = None

            expected_sort = ('-priority',)

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        _using_string()

    def test_query_field(self):
        
        def _using_list():
            query_dict = {
                DAOQuery.FIELDS: ['code', 'priority']
            }

            expected_query_filter = None

            expected_fields = {"$project": {'code':1, 'priority': 1}}

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        _using_list()

        def _using_one_item_list():
            query_dict = {
                DAOQuery.FIELDS: ['priority']
            }

            expected_query_filter = None

            expected_fields = {"$project": {'priority': 1}}

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        _using_one_item_list()

        def _using_string():
            query_dict = {
                DAOQuery.FIELDS: 'priority'
            }

            expected_query_filter = None

            expected_fields = {"$project": {'priority': 1}}

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == DAOQuery().build(**query_dict)

        _using_string()
    