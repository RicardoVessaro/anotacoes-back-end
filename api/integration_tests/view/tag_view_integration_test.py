
from api.integration_tests.constants import TAG_URL
from ipsum.util.test.view.enum_integration_test import EnumIntegrationTest
from ipsum.util.test.view.view_integration_test import PaginateFilterResult
from ipsum.view.ipsum_view import QUERY_LIMIT, QUERY_OFFSET, QUERY_SORT

class TestTagView(EnumIntegrationTest):

    expected_enums = [
        {'id': '62df2767730a8633f2fec97f', 'code': 1, 'name': "IMPORTANT"},
        {'id': '62b3565f0d2ae186982e9746', 'code': 2, 'name': "OK"},
        {'id': '62b356600d2ae186982e9747', 'code': 3, 'name': "LATER"},
    ]
    
    base_url = TAG_URL

    filter_to_not_found = {"name": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(3), offset=0, limit=5, total=3, empty=False),
        PaginateFilterResult(filter={QUERY_LIMIT:2}, expected_indexes=range(2),  offset=0, limit=2, total=3, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:2, QUERY_LIMIT:2}, expected_indexes=range(2,3), offset=2, limit=2, total=3, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:1, QUERY_LIMIT:2, "code[or:eq]": list(range(1, 3))}, expected_indexes=[1], offset=1, limit=2, total=2, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:0, QUERY_LIMIT:2, QUERY_SORT: '-code'}, expected_indexes=range(1,3), offset=0, limit=2, total=3, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:0, QUERY_LIMIT:2, QUERY_SORT: ['-code']}, expected_indexes=range(1,3), offset=0, limit=2, total=3, empty=False),
        PaginateFilterResult(filter={'code[in]': [1,2]}, expected_indexes=[0,1], offset=0, limit=5, total=2, empty=False)
    ]
