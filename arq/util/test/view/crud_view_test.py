
import requests

from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import ArqViewTest
from arq.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE


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

    def test_update(self):
        db_model = self.get_model()

        database_test = DatabaseTest()
        database_test.add_data(self.dao, db_model)
    
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            id = str(db_model.id)
            url = self.get_view_url() + f'/{id}'

            updated_model = self.get_updated_model()
            updated_model.id = db_model.id

            data = self.encode(updated_model)

            response = requests.put(url, json=data)

            item = response.json()

            for k in data:
                assert data[k] == item[k]

        _()

        def _must_return_404_not_found_when_id_not_exists():
            url = self.get_view_url() + f'/{self.fake_id}'

            updated_model = self.get_updated_model()
            updated_model.id = db_model.id

            data = self.encode(updated_model)

            response = requests.put(url, json=data)

            assert response.status_code == 404

            item = response.json()

            assert item['status_code'] == 404
            assert item['message'] == OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self.fake_id)

        _must_return_404_not_found_when_id_not_exists()

    def test_delete(self):
        db_model = self.get_model()

        database_test = DatabaseTest()
        database_test.add_data(self.dao, db_model)
    
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            id = str(db_model.id)

            url = self.get_view_url() + f'/{id}'

            response = requests.delete(url)

            assert response.status_code == 204

            assert_response = requests.get(url)

            assert assert_response.status_code == 204

        _()
        
        def _must_return_404_not_found_when_id_not_exists():
            
            url = self.get_view_url() + f'/{self.fake_id}'

            response = requests.delete(url)

            assert response.status_code == 404

            item = response.json()

            assert item['status_code'] == 404
            assert item['message'] == OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self.fake_id)

        _must_return_404_not_found_when_id_not_exists()
