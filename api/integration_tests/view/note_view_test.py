
import requests

from datetime import datetime
from api.annotation.service.mood.mood_service import BORING, COOL, GREAT, SAD
from api.annotation.service.note.note_service import CREATED_IN, TAG
from api.annotation.service.tag.tag_service import IMPORTANT, OK
from ipsum.util.data.pagination import Pagination
from ipsum.util.test.database_test import DatabaseTest
from ipsum.util.test.view.ipsum_view_test import  PaginateFilterResult
from api.annotation.view.note_view import NoteView
from ipsum.util.test.view.crud_view_test import CRUDViewTest
from api.annotation.view.tag_view import tag_view_name
from api.annotation.view.mood_view import mood_view_name



class TestNoteView(CRUDViewTest):

    view = NoteView()

    filter_to_not_found = {"title": "to not found"}

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), offset=0, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={"pinned":False}, expected_indexes=range(8, 13), offset=0, limit=5, total=7, empty=False),
        PaginateFilterResult(filter={"_limit":7}, expected_indexes=range(7),  offset=0, limit=7, total=15, empty=False),
        PaginateFilterResult(filter={"_offset":5, "_limit":5},  expected_indexes=range(5,10), offset=5, limit=5, total=15, empty=False),
        PaginateFilterResult(filter={"pinned":False, "_offset":6, "_limit":6}, expected_indexes=[14], offset=6, limit=6, total=7, empty=False),
        PaginateFilterResult(filter={"_offset":14, "_limit":7},  expected_indexes=[14], offset=14, limit=7, total=15, empty=False)
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
            url = self.get_view_url()

            ok_tag = self._find_enum_by_code(tag_view_name, OK.code)
            db_model = self.get_model()
            db_model.created_in = None

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

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
            url = self.get_view_url()

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

        response_j = requests.get(enum_find_by_code_url).json()[Pagination.ITEMS_KEY]

        return response_j[0]

    def _get_enum_find_by_code_url(self, enum_view_name, code):
        return f'{self.get_view_url(with_view_name=False)}{enum_view_name}?code={code}'   
