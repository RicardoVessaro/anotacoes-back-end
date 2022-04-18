
import requests

from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import ArqViewTest


class CRUDViewTest(ArqViewTest):

    def test_insert(self):

        database_test = DatabaseTest(daos_to_clean=[self.dao])
        
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            url = self.get_view_url() + '/'

            db_model = self.get_model()

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

            for k in data:
                assert data[k] == item[k]

        _()

