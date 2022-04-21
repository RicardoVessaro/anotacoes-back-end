
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.view.arq_view_test import FindFilterResult, PaginateFilterResult
from arq.util.test.view.crud_view_test import CRUDViewTest
from api.modules.core.blueprints.view.tag_view import tag_view_name
from api.modules.core.blueprints.data.model.tag import Tag
from api.modules.core.blueprints.data.dao.tag_dao import TagDAO

class TestTagView(CRUDViewTest):

    INTEGRATION_TEST_DB_URI = get_test_database_url()

    view_name = tag_view_name

    model = Tag

    dao = TagDAO()

    find_filter_results = [
        FindFilterResult(filter={}, expected_indexes=range(3)),
        FindFilterResult(filter={"name":"test 2"}, expected_indexes=[2]),
        FindFilterResult(filter={"name":["test 0", "test 1"]}, expected_indexes=[0,1]),
        FindFilterResult(filter={"code": 2}, expected_indexes=[2]),
        FindFilterResult(filter={"code":[0, 1]}, expected_indexes=[0,1]),
        FindFilterResult(filter={"priority": 0}, expected_indexes=[0]),
        FindFilterResult(filter={"priority":[1, 2]}, expected_indexes=[1,2])
    ]

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), pages=3, page=1, limit=5, total=15, has_prev=False, has_next=True),
        PaginateFilterResult(filter={"limit":7}, expected_indexes=range(7),  pages=3, page=1, limit=7, total=15, has_prev=False, has_next=True),
        PaginateFilterResult(filter={"page":2, "limit":5},  pages=3, expected_indexes=range(5,10), page=2, limit=5, total=15, has_prev=True, has_next=True),
        PaginateFilterResult(filter={"page":3, "limit":7},  pages=3, expected_indexes=[14], page=3, limit=7, total=15, has_prev=True, has_next=False),
        PaginateFilterResult(filter={"page":2, "limit":7, "code": list(range(10))},  pages=2, expected_indexes=[7,8,9], page=2, limit=7, total=10, has_prev=True, has_next=False)
    ]

    def get_model(self):
        return self.model(
            code=1,
            name="test",
            priority="1"
        )

    def get_updated_model(self):
        return self.model(
            code=1,
            name="test UPDATED",
            priority=1
        )


    def find_model_list(self):
        model_list = []

        for i in range(3):

            db_model = self.model(
                code=i,
                name=f"test {i}",
                priority=i
            )

            model_list.append(db_model)

        return model_list

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