
from ipsum.util.test.view.detail_crud_view_test import DetailCRUDViewTest
from api.annotation.view.picture_view import PictureView
from ipsum.util.test.view.ipsum_view_test import PaginateFilterResult
from ipsum.view.ipsum_view import QUERY_OFFSET


class TestPictureView(DetailCRUDViewTest):

    view = PictureView()

    filter_to_not_found = {"title": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(8,13), offset=0, limit=5, total=7, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:5}, expected_indexes=range(13,15), offset=5, limit=5, total=7, empty=False),
        PaginateFilterResult(filter={"title":"Picture 9"}, expected_indexes=[9], offset=0, limit=5, total=1, empty=False),
        PaginateFilterResult(filter={"title":["Picture 10", "Picture 11"]}, expected_indexes=[10, 11], offset=0, limit=5, total=2, empty=False)
    ]

    def get_model(self):
        return self.model(
            title = 'Test Picture',
            note_id = self.fake_parent_id,
            created_in = '2022-06-04T20:46:00.000000'
        )

    def get_parent_model(self):
        return self.parent_dao.model(
            id=self.fake_parent_id,
            title="test",
            pinned=False,
            text="lorem ipsum dolor sit amet",
        )

    def get_updated_model(self):
        return self.model(
            title = 'Updated Picture',
            note_id = self.fake_parent_id
        )

    def model_list(self):
        model_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(15):

            parent_id = self.fake_parent_id
            if i < 8:
                parent_id = other_parent_id

            db_model = self.model(
                title = f'Picture {i}',
                note_id = parent_id
            )

            model_list.append(db_model)

        return model_list
