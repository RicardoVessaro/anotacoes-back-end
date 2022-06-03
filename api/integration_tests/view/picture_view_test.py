
from api.annotation.data.model.picture import Picture
from api.annotation.data.dao.picture_dao import PictureDAO
from api.annotation.general.module_constants import REST_API_V1_BASE_URL
from api.annotation.service.note.note_service import NoteService
from api.annotation.service.note.picture.picture_service import PictureService
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.view.detail_crud_view_test import DetailCRUDViewTest
from api.annotation.view.picture_view import PictureView, picture_view_name
from arq.util.test.view.ipsum_view_test import FindFilterResult, PaginateFilterResult
from api.annotation.data.dao.note_dao import NoteDAO
from arq.util.view.route_parser import parse_route


class TestPictureView(DetailCRUDViewTest):

    view = PictureView()

    filter_to_not_found = {"title": "to not found"}

    find_filter_results = [
        FindFilterResult(filter={}, expected_indexes=range(3)),
        FindFilterResult(filter={"title":"Picture 1"}, expected_indexes=[1]),
        FindFilterResult(filter={"title":["Picture 1", "Picture 2" ] }, expected_indexes=[1,2]),
        FindFilterResult(filter={"title":"Picture 4"}, expected_indexes=[])
    ]

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(8,13), pages=2, page=1, limit=5, total=7, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"page":2}, expected_indexes=range(13,15), pages=2, page=2, limit=5, total=7, has_prev=True, has_next=False, has_result=True),
        PaginateFilterResult(filter={"title":"Picture 9"}, expected_indexes=[9], pages=1, page=1, limit=5, total=1, has_prev=False, has_next=False, has_result=True),
        PaginateFilterResult(filter={"title":["Picture 10", "Picture 11"]}, expected_indexes=[10, 11], pages=1, page=1, limit=5, total=2, has_prev=False, has_next=False, has_result=True)
    ]

    def get_model(self):
        return self.model(
            title = 'Test Picture',
            note_id = self.fake_parent_id
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

    def find_model_list(self):
        model_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(6):

            parent_id = self.fake_parent_id
            if i > 2:
                parent_id = other_parent_id

            db_model = self.model(
                title = f'Picture {i}',
                note_id = parent_id
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
                title = f'Picture {i}',
                note_id = parent_id
            )

            model_list.append(db_model)

        return model_list