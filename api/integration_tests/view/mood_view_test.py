
from api.annotation.service.mood.mood_service import MoodService
from ipsum.util.test.view.crud_view_test import CRUDViewTest
from ipsum.util.test.view.ipsum_view_test import PaginateFilterResult
from api.annotation.view.mood_view import MoodView
from ipsum.view.ipsum_view import QUERY_LIMIT, QUERY_OFFSET, QUERY_SORT

class TestMoodView(CRUDViewTest):

    view = MoodView()

    filter_to_not_found = {"name": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_LIMIT:7}, expected_indexes=range(7),  offset=0, limit=7, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:5, QUERY_LIMIT:5}, expected_indexes=range(5,10), offset=5, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:14, QUERY_LIMIT:7}, expected_indexes=[14], offset=14, limit=7, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:7, QUERY_LIMIT:7, "code[or:eq]": list(range(10))}, expected_indexes=[7,8,9], offset=7, limit=7, total=10, empty=False),
        PaginateFilterResult(filter={QUERY_SORT: '-code'}, expected_indexes=range(10,15), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_SORT: ['-code']}, expected_indexes=range(10,15), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={'code[gte]': 3, 'code[lte]': 7}, expected_indexes=range(3, 8), offset=0, limit=5, total=5, empty=False)
    ]

    def get_model(self):
        return self.model(
            code=-1,
            name="test"
        )

    def get_updated_model(self):
        return self.model(
            code=-1,
            name="test UPDATED"
        )

    def model_list(self):
        model_list = []

        for i in range(15):

            db_model = self.model(
                code=i,
                name=f"test {i}"
            )

            model_list.append(db_model)

        return model_list
