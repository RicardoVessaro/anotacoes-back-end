
from ipsum.util.data.query_filter import QueryFilter


class TestQueryFilter:

    def test_query_filter_builder_when_not_using_list_or_tuple(self):
        query_dict = {
            'name': "John",
            'number': "1"
        }

        expected_query_filter = {
            'name': "John",
            'number': "1"
        }

        expected_fields = None

        expected_query_sort = None

        assert (expected_query_filter, expected_fields, expected_query_sort) == QueryFilter().build(**query_dict)

    def test_query_filter_builder_when_using_list(self):
        query_dict = {
            'name': "John",
            'number': "1",
            'color': ["Blue", "Red"]
        }

        expected_query_filter = {
            'name': "John",
            'number': "1",
            'color__in': ["Blue", "Red"]
        }

        expected_fields = None

        expected_query_sort = None

        assert (expected_query_filter, expected_fields, expected_query_sort) == QueryFilter().build(**query_dict)

    def test_query_filter_builder_when_using_tuple(self):
        query_dict = {
            'name': "John",
            'number': "1",
            'color': ("Blue", "Red")
        }

        expected_query_filter = {
            'name': "John",
            'number': "1",
            'color__in': ("Blue", "Red")
        }

        expected_fields = None

        expected_query_sort = None

        assert (expected_query_filter, expected_fields, expected_query_sort) == QueryFilter().build(**query_dict)
        
    def test_query_filter_sort(self):
        
        def _using_list():
            query_dict = {
                'name': "John",
                'number': "1",
                QueryFilter.SORT: ['code', '-priority']
            }

            expected_query_filter = {
                'name': "John",
                'number': "1"
            }

            expected_fields = None

            expected_sort = ('code', '-priority')

            assert (expected_query_filter, expected_fields, expected_sort) == QueryFilter().build(**query_dict)

        _using_list()

        def _using_one_item_list():
            query_dict = {
                'name': "John",
                'number': "1",
                QueryFilter.SORT: ['-priority']
            }

            expected_query_filter = {
                'name': "John",
                'number': "1"
            }

            expected_fields = None

            expected_sort = ('-priority',)

            assert (expected_query_filter, expected_fields, expected_sort) == QueryFilter().build(**query_dict)

        _using_one_item_list()

        def _using_string():
            query_dict = {
                'name': "John",
                'number': "1",
                QueryFilter.SORT: '-priority'
            }

            expected_query_filter = {
                'name': "John",
                'number': "1"
            }

            expected_fields = None

            expected_sort = ('-priority',)

            assert (expected_query_filter, expected_fields, expected_sort) == QueryFilter().build(**query_dict)

        _using_string()

    def test_query_filter_field(self):
        
        def _using_list():
            query_dict = {
                'name': "John",
                'number': "1",
                QueryFilter.FIELDS: ['code', 'priority']
            }

            expected_query_filter = {
                'name': "John",
                'number': "1"
            }

            expected_fields = {"$project": {'code':1, 'priority': 1}}

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == QueryFilter().build(**query_dict)

        _using_list()

        def _using_one_item_list():
            query_dict = {
                'name': "John",
                'number': "1",
                QueryFilter.FIELDS: ['priority']
            }

            expected_query_filter = {
                'name': "John",
                'number': "1"
            }

            expected_fields = {"$project": {'priority': 1}}

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == QueryFilter().build(**query_dict)

        _using_one_item_list()

        def _using_string():
            query_dict = {
                'name': "John",
                'number': "1",
                QueryFilter.FIELDS: 'priority'
            }

            expected_query_filter = {
                'name': "John",
                'number': "1"
            }

            expected_fields = {"$project": {'priority': 1}}

            expected_sort = None

            assert (expected_query_filter, expected_fields, expected_sort) == QueryFilter().build(**query_dict)

        _using_string()
    