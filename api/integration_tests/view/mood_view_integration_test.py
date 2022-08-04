

from api.integration_tests.constants import MOOD_URL
from ipsum.util.test.view.enum_integration_test import EnumIntegrationTest
from ipsum.util.test.view.view_integration_test import PaginateFilterResult
from ipsum.view.ipsum_view import QUERY_LIMIT, QUERY_OFFSET, QUERY_SORT


class TestMoodView(EnumIntegrationTest):

    base_url = MOOD_URL

    expected_enums = [
        {'id': '62b356430d2ae186982e96ef', 'code': 1, 'name': "Cool"},
        {'id': '62b356430d2ae186982e96f0', 'code': 2, 'name': "Ok"},
        {'id': '62b356430d2ae186982e96f1', 'code': 3, 'name': "Boring"},
        {'id': '62b356430d2ae186982e96f2', 'code': 4, 'name': "Sad"},
        {'id': '62b356430d2ae186982e96f3', 'code': 5, 'name': "Love"},
        {'id': '62b356430d2ae186982e96f4', 'code': 6, 'name': "Great"},
    ]

    filter_to_not_found = {"name": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), offset=0, limit=5, total=6, empty=False),
        PaginateFilterResult(filter={QUERY_LIMIT:6}, expected_indexes=range(6),  offset=0, limit=6, total=6, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:5, QUERY_LIMIT:5}, expected_indexes=range(5,6), offset=5, limit=5, total=6, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:3, QUERY_LIMIT:3}, expected_indexes=range(3,6), offset=3, limit=3, total=6, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:3, QUERY_LIMIT:3, "code[or:eq]": list(range(3,7))}, expected_indexes=range(5,6), offset=3, limit=3, total=4, empty=False),
        PaginateFilterResult(filter={QUERY_SORT: '-code'}, expected_indexes=range(1,6), offset=0, limit=5, total=6, empty=False),
        PaginateFilterResult(filter={QUERY_SORT: ['-code']}, expected_indexes=range(1,6), offset=0, limit=5, total=6, empty=False),
        PaginateFilterResult(filter={'code[gte]': 3, 'code[lte]': 7}, expected_indexes=range(2, 6), offset=0, limit=5, total=4, empty=False)
    ]
