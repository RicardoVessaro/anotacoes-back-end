
from ipsum.util.test.view.ipsum_view_test import PaginateFilterResult
from ipsum.util.test.view.crud_view_test import CRUDViewTest
from api.annotation.view.tag_view import TagView

class TestTagView(CRUDViewTest):

    view = TagView()

    filter_to_not_found = {"name": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), pages=3, page=1, limit=5, total=15, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"limit":7}, expected_indexes=range(7),  pages=3, page=1, limit=7, total=15, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"page":2, "limit":5},  pages=3, expected_indexes=range(5,10), page=2, limit=5, total=15, has_prev=True, has_next=True, has_result=True),
        PaginateFilterResult(filter={"page":3, "limit":7},  pages=3, expected_indexes=[14], page=3, limit=7, total=15, has_prev=True, has_next=False, has_result=True),
        PaginateFilterResult(filter={"page":2, "limit":7, "code": list(range(10))},  pages=2, expected_indexes=[7,8,9], page=2, limit=7, total=10, has_prev=True, has_next=False, has_result=True)
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

    def paginate_model_list(self):
        model_list = []

        for i in range(15):

            db_model = self.model(
                code=i,
                name=f"test {i}",
                priority=i
            )

            model_list.append(db_model)

        return model_list
