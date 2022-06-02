
from arq.util.test.view.arq_view_test import FindFilterResult, PaginateFilterResult
from arq.util.test.view.detail_crud_view_test import DetailCRUDViewTest
from api.modules.core.blueprints.view.comment_view import CommentView

class TestCommentView(DetailCRUDViewTest):

    view = CommentView()

    filter_to_not_found = {"comment": "to not found"}

    find_filter_results = [
        FindFilterResult(filter={}, expected_indexes=range(3)),
        FindFilterResult(filter={"comment":"Comment 1"}, expected_indexes=[1]),
        FindFilterResult(filter={"comment":["Comment 1", "Comment 2" ] }, expected_indexes=[1,2]),
        FindFilterResult(filter={"comment":"Comment 4"}, expected_indexes=[])
    ]

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(8,13), pages=2, page=1, limit=5, total=7, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"page":2}, expected_indexes=range(13,15), pages=2, page=2, limit=5, total=7, has_prev=True, has_next=False, has_result=True),
        PaginateFilterResult(filter={"comment":"Comment 9"}, expected_indexes=[9], pages=1, page=1, limit=5, total=1, has_prev=False, has_next=False, has_result=True),
        PaginateFilterResult(filter={"comment":["Comment 10", "Comment 11"]}, expected_indexes=[10, 11], pages=1, page=1, limit=5, total=2, has_prev=False, has_next=False, has_result=True)
    ]

    def get_model(self):
        return self.model(
            comment = 'Test Comment',
            picture_id = self.fake_parent_id
        )

    def get_parent_model(self):
        return self.parent_dao.model(
            id = self.fake_parent_id,
            title = 'Test Picture'
        )

    def get_updated_model(self):
        return self.model(
            comment = 'Updated Comment',
            picture_id = self.fake_parent_id
        )

    def find_model_list(self):
        model_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(6):

            parent_id = self.fake_parent_id
            if i > 2:
                parent_id = other_parent_id

            db_model = self.model(
                comment = f'Comment {i}',
                picture_id = parent_id
            )

            model_list.append(db_model)

        return model_list

    def paginate_model_list(self):
        model_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(15):

            parent_id = self.fake_parent_id
            if i < 8:
                parent_id = other_parent_id

            db_model = self.model(
                comment = f'Comment {i}',
                picture_id = parent_id
            )

            model_list.append(db_model)

        return model_list