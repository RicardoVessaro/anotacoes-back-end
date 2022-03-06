
from arq.util.data.query_filter_builder import QueryFilterBuilder


class TestQueryFilterBuilder:

    def test_query_filter_builder_when_not_using_list_or_tuple(self):
        query_dict = {
            'name': "John",
            'number': "1"
        }

        assert query_dict == QueryFilterBuilder().build(query_dict)

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

        assert expected_query_filter == QueryFilterBuilder().build(query_dict)

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

        assert expected_query_filter == QueryFilterBuilder().build(query_dict)
        
