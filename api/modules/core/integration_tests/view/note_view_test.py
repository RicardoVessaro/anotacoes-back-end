
import requests

from datetime import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import ArqViewTest, FindFilterResult, PaginateFilterResult
from api.modules.core.blueprints.data.model.note import Note
from api.modules.core.blueprints.view.note_view import note_view_name

class TestNoteView(ArqViewTest):

    INTEGRATION_TEST_DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-integration-test?retryWrites=true&w=majority"

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

        db_model = self.model(
            title="test",
            pinned=False,
            text="lorem ipsum dolor sit amet",
            created_in=created_in
        )
        
        return db_model

    def get_updated_model(self):
        db_model = self.model(
            title="test UPDATED",
            pinned=True,
            text="lorem ipsum dolor sit amet UPDATED",
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
        CREATED_IN = 'created_in'

        database_test = DatabaseTest(daos_to_clean=[self.dao])
        
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            url = self.get_view_url() + '/'

            db_model = self.get_model()
            db_model.created_in = None

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

            for k in data:
                if k != CREATED_IN:
                    assert data[k] == item[k]

            assert not item[CREATED_IN] is None

        _()
        