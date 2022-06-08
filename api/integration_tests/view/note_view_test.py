
import pytest
import requests

from datetime import datetime
from api.annotation.data.dao.note_dao import NoteDAO
from api.annotation.service.mood.mood_service import BORING, COOL, GREAT, SAD, MoodService
from api.annotation.service.note.note_service import CREATED_IN, TAG, NoteService
from api.annotation.service.tag.tag_service import IMPORTANT, OK, TagService
from ipsum.util.enviroment_variable import get_api_url, get_test_database_url
from ipsum.util.test.database_test import DatabaseTest
from ipsum.util.test.view.ipsum_view_test import FindFilterResult, PaginateFilterResult
from api.annotation.data.model.note import Note
from api.annotation.view.note_view import NoteView, note_view_name
from ipsum.util.test.view.crud_view_test import CRUDViewTest
from api.annotation.view.tag_view import tag_view_name
from api.annotation.view.mood_view import mood_view_name



class TestNoteView(CRUDViewTest):

    view = NoteView()

    filter_to_not_found = {"title": "to not found"}

    find_filter_results = [
        FindFilterResult(filter={}, expected_indexes=range(3)),
        FindFilterResult(filter={"pinned":True}, expected_indexes=[0,2]),
        FindFilterResult(filter={"pinned":False}, expected_indexes=[1]),
        FindFilterResult(filter={"title":"test 2"}, expected_indexes=[2]),
        FindFilterResult(filter={"title":["test 0", "test 1"]}, expected_indexes=[0,1])
    ]

    paginate_filter_results = [
        PaginateFilterResult(filter={}, expected_indexes=range(5), pages=3, page=1, limit=5, total=15, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"pinned":False}, expected_indexes=range(8, 13), pages=2, page=1, limit=5, total=7, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"limit":7}, expected_indexes=range(7),  pages=3, page=1, limit=7, total=15, has_prev=False, has_next=True, has_result=True),
        PaginateFilterResult(filter={"page":2, "limit":5},  pages=3, expected_indexes=range(5,10), page=2, limit=5, total=15, has_prev=True, has_next=True, has_result=True),
        PaginateFilterResult(filter={"pinned":False, "page":2, "limit":6},  pages=2, expected_indexes=[14], page=2, limit=6, total=7, has_prev=True, has_next=False, has_result=True),
        PaginateFilterResult(filter={"page":3, "limit":7},  pages=3, expected_indexes=[14], page=3, limit=7, total=15, has_prev=True, has_next=False, has_result=True)
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

        response_j = requests.get(enum_find_by_code_url).json()

        return response_j[0]

    def _get_enum_find_by_code_url(self, enum_view_name, code):
        return f'{self.get_view_url(with_view_name=False)}{enum_view_name}?code={code}'   

