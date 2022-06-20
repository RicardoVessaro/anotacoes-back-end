
from ipsum.util.test.view.ipsum_view_test import PaginateFilterResult
from ipsum.util.test.view.crud_view_test import CRUDViewTest
from api.annotation.view.tag_view import TagView
from ipsum.view.ipsum_view import QUERY_LIMIT, QUERY_OFFSET, QUERY_SORT

class TestTagView(CRUDViewTest):

    view = TagView()

    filter_to_not_found = {"name": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_LIMIT:7}, expected_indexes=range(7),  offset=0, limit=7, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:5, QUERY_LIMIT:5}, expected_indexes=range(5,10), offset=5, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:14, QUERY_LIMIT:7}, expected_indexes=[14], offset=14, limit=7, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:7, QUERY_LIMIT:7, "code[or:eq]": list(range(10))}, expected_indexes=[7,8,9], offset=7, limit=7, total=10, empty=False),
        PaginateFilterResult(filter={QUERY_SORT: '-code'}, expected_indexes=range(10,15), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={QUERY_SORT: ['-code']}, expected_indexes=range(10,15), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={'code[in]': [0,1,2]}, expected_indexes=[0,1,2], offset=0, limit=5, total=3, empty=False)
    ]

    def get_model(self):
        return self.model(
            code=-1,
            name="test",
            priority="1"
        )

    def get_updated_model(self):
        return self.model(
            code=-1,
            name="test UPDATED",
            priority=1
        )

    def model_list(self):
        model_list = []

        for i in range(15):

            db_model = self.model(
                code=i,
                name=f"test {i}",
                priority=i
            )

            model_list.append(db_model)

        return model_list
