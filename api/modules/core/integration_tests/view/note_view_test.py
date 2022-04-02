
import requests

from datetime import datetime
from api.modules.core.blueprints.data.dao.note_dao import NoteDAO
from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import ArqViewTest
from api.modules.core.blueprints.data.model.note import Note
from api.modules.core.blueprints.view.note_view import note_view_name

class TestNoteView(ArqViewTest):

    INTEGRATION_TEST_DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-integration-test?retryWrites=true&w=majority"

    view_name = note_view_name

    model = Note

    dao = NoteDAO()

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

    def test_insert(self):
        CREATED_IN = 'created_in'

        database_test = DatabaseTest(daos_to_clean=[self.dao])
        
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            url = self._get_view_url() + '/'

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
        