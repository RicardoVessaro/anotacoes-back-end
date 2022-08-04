
from api.integration_tests.constants import COMMENT_URL, FAKE_NOTE_ID, FAKE_PICTURE_ID, NOTE_URL, PICTURE_URL
from ipsum.util.enviroment_variable import get_api_url
from ipsum.util.test.view.detail_crud_integration_test import DependencyParent, DetailCRUDIntegrationTest
from ipsum.util.test.view.view_integration_test import PaginateFilterResult
from ipsum.view.ipsum_view import QUERY_OFFSET


class TestCommentView(DetailCRUDIntegrationTest):

    base_url = COMMENT_URL

    body = {
        'comment': 'Comment Integration Test',
        'picture_id': FAKE_PICTURE_ID
    }

    update_body = {
        'comment': 'Comment Integration Test Updated',
        'picture_id': FAKE_PICTURE_ID
    }

    filter_to_not_found = {"comment": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(8,13), offset=0, limit=5, total=7, empty=False),
        PaginateFilterResult(filter={QUERY_OFFSET:5}, expected_indexes=range(13,15), offset=5, limit=5, total=7, empty=False),
        PaginateFilterResult(filter={"comment":"Comment 9"}, expected_indexes=[9], offset=0, limit=5, total=1, empty=False),
        PaginateFilterResult(filter={"comment[or:eq]":["Comment 10", "Comment 11"]}, expected_indexes=[10, 11], offset=0, limit=5, total=2, empty=False)
    ]

    dependency_parents = [
        DependencyParent(f'{get_api_url()}/{NOTE_URL}', {
            'id': FAKE_NOTE_ID,
            'title': 'Note Integration Test',
            'text': 'Loren ipsum dolor sit amet',
            'tag': '62dbd88ab6e09960b225c5ec',
            'moods': ['62dbd8e9b6e09960b225c5ed', '62dc062a3141aa4d53f507e3'],
            'pinned': True
        })
    ]

    parent_field = 'picture_id'

    parent_base_url = PICTURE_URL

    parent_body = {
        'id': FAKE_PICTURE_ID,
        'title': 'Picture Integration Test',
        'note_id': FAKE_NOTE_ID,
        'created_in': '2022-06-04T20:46:00'
    }

    def body_list(self):
        body_list = []

        other_parent_id = '624786f6590c79c2fb3af557'

        for i in range(15):

            parent_id = FAKE_PICTURE_ID
            if i < 8:
                parent_id = other_parent_id

            body = {
                'comment': f'Comment {i}',
                'picture_id': parent_id
            }

            body_list.append(body)

        return body_list
    