
import requests

from datetime import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from api.modules.core.blueprints.service.mood.mood_service import BORING, COOL, GREAT, SAD, MoodService
from api.modules.core.blueprints.service.note.note_service import CREATED_IN, TAG
from api.modules.core.blueprints.service.tag.tag_service import IMPORTANT, OK, TagService
from arq.util.enviroment_variable import get_api_url, get_test_database_url
from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import FindFilterResult, PaginateFilterResult
from api.modules.core.blueprints.data.model.note import Note
from api.modules.core.blueprints.view.note_view import note_view_name
from arq.util.test.view.crud_view_test import CRUDViewTest
from api.modules.core.blueprints.view.tag_view import tag_view_name
from api.modules.core.blueprints.view.mood_view import mood_view_name

class TestNoteView(CRUDViewTest):

    INTEGRATION_TEST_DB_URI = get_test_database_url()

    enum_services_to_insert = [TagService(), MoodService()]

    view_name = note_view_name

    model = Note

    dao = NoteDAO()

    find_filter_results = [
        FindFilterResult(filter={}, expected_indexes=range(3)),
        FindFilterResult(filter={"pinned":True}, expected_indexes=[0,2]),
        FindFilterResult(filter={"pinned":False}, expected_indexes=[1]),
        FindFilterResult(filter={"title":"test 2"}, expected_indexes=[2]),
        FindFilterResult(filter={"title":["test 0", "test 1"]}, expected_indexes=[0,1])
    ]

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), pages=3, page=1, limit=5, total=15, has_prev=False, has_next=True),
        PaginateFilterResult(filter={"pinned":False}, expected_indexes=range(8, 13), pages=2, page=1, limit=5, total=7, has_prev=False, has_next=True),
        PaginateFilterResult(filter={"limit":7}, expected_indexes=range(7),  pages=3, page=1, limit=7, total=15, has_prev=False, has_next=True),
        PaginateFilterResult(filter={"page":2, "limit":5},  pages=3, expected_indexes=range(5,10), page=2, limit=5, total=15, has_prev=True, has_next=True),
        PaginateFilterResult(filter={"pinned":False, "page":2, "limit":6},  pages=2, expected_indexes=[14], page=2, limit=6, total=7, has_prev=True, has_next=False),
        PaginateFilterResult(filter={"page":3, "limit":7},  pages=3, expected_indexes=[14], page=3, limit=7, total=15, has_prev=True, has_next=False)
    ]

    def get_model(self):
        created_in_str = '02/04/2022'

        created_in = datetime.strptime(created_in_str, '%d/%m/%Y')

        sad_mood = self._find_enum_by_code(mood_view_name, SAD.code)
        boring_mood = self._find_enum_by_code(mood_view_name, BORING.code)

        db_model = self.model(
            title="test",
            pinned=False,
            text="lorem ipsum dolor sit amet",
            created_in=created_in,
            moods=[sad_mood['id'], boring_mood['id']]
        )
        
        return db_model

    def get_updated_model(self):

        important_tag = self._find_enum_by_code(tag_view_name, IMPORTANT.code)

        cool_mood = self._find_enum_by_code(mood_view_name, COOL.code)
        great_mood = self._find_enum_by_code(mood_view_name, GREAT.code)

        db_model = self.model(
            title="test UPDATED",
            pinned=True,
            text="lorem ipsum dolor sit amet UPDATED",
            tag=important_tag['id'],
            moods=[cool_mood['id'], great_mood['id']]
        )
        
        return db_model 

    def find_model_list(self):
        model_list = []

        pinned = True
        for i in range(3):

            db_model = self.model(
                title=f"test {i}",
                pinned=pinned,
                text=f"lorem ipsum dolor sit amet {i}",
            )

            pinned = not pinned

            model_list.append(db_model)

        return model_list

    def paginate_model_list(self):
        model_list = []

        pinned = True
        for i in range(15):

            db_model = self.model(
                title=f"test {i}",
                pinned=pinned,
                text=f"lorem ipsum dolor sit amet {i}",
            )

            pinned = i < 7

            model_list.append(db_model)

        return model_list

    def test_insert(self):
        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.dao])
        
        @database_test.persistence_test()
        def _():
            url = self.get_view_url() + '/'

            db_model = self.get_model()
            db_model.created_in = None

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

            ok_tag = self._find_enum_by_code(tag_view_name, OK.code)

            for k in data:
                if k != CREATED_IN:
                    assert data[k] == item[k]

            assert not item[CREATED_IN] is None

            assert ok_tag['id'] == item['tag']
        _()
        
    def test_insert_with_default_values(self):
        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.dao])
        
        @database_test.persistence_test()
        def _():
            url = self.get_view_url() + '/'

            db_model = self.get_model()

            important_tag = self._find_enum_by_code(tag_view_name, IMPORTANT.code)
            db_model[TAG] = important_tag['id']

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

            for k in data:
                if k != CREATED_IN:
                    assert data[k] == item[k]

            assert not item[CREATED_IN] is None
        _()

    def _find_enum_by_code(self, enum_view_name, code):
        enum_find_by_code_url = self._get_enum_find_by_code_url(enum_view_name, code)

        response_j = requests.get(enum_find_by_code_url).json()

        return response_j[0]

    def _get_enum_find_by_code_url(self, enum_view_name, code):
        return f'{get_api_url()}/{enum_view_name}?code={code}'   

