
import requests

from abc import ABC, abstractproperty, abstractmethod
from datetime import datetime
from arq.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from arq.util.test.integration_test import get_base_url
from arq.util.test.database_test import DatabaseTest
from arq.util.view.view_encoder import ViewEncoder

# Fazer classe gegnerica para testar tag e note
#   pois nao havera teste de inntegracao para estrutura da ARQ

ID_FIELD = 'id'

class ArqViewTest(ABC):

    fake_id = '6248620366564103f229595f'

    @abstractproperty
    def INTEGRATION_TEST_DB_URI(self):
        pass

    @abstractproperty        
    def view_name(self):
        pass

    @abstractproperty
    def model(self):
        pass

    @abstractproperty
    def dao(self):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def get_updated_model(self):
        pass

    def test_insert(self):

        database_test = DatabaseTest(daos_to_clean=[self.dao])
        
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            url = self._get_view_url() + '/'

            db_model = self.get_model()

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

            for k in data:
                assert data[k] == item[k]

        _()


    def test_find_by_id(self):
        db_model = self.get_model()

        database_test = DatabaseTest()
        database_test.add_data(self.dao, db_model)
    
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            id = str(db_model.id)
            url = self._get_view_url() + f'/{id}'

            response = requests.get(url)

            item = response.json()

            dict_model = self.encode(db_model)

            for k in item:
                assert item[k] == dict_model[k]
        _()

        def _must_return_204_no_content_when_id_not_exists():

            url = self._get_view_url() + f'/{self.fake_id}'

            response = requests.get(url)

            assert response.status_code == 204

        _must_return_204_no_content_when_id_not_exists()

    def test_update(self):
        db_model = self.get_model()

        database_test = DatabaseTest()
        database_test.add_data(self.dao, db_model)
    
        @database_test.persistence_test(host=self.INTEGRATION_TEST_DB_URI)
        def _():
            id = str(db_model.id)
            url = self._get_view_url() + f'/{id}'

            updated_model = self.get_updated_model()
            updated_model.id = db_model.id

            data = self.encode(updated_model)

            response = requests.put(url, json=data)

            item = response.json()

            for k in data:
                assert data[k] == item[k]

        _()

        def _must_return_404_not_found_when_id_not_exists():
            url = self._get_view_url() + f'/{self.fake_id}'

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

            url = self._get_view_url() + f'/{id}'

            response = requests.delete(url)

            assert response.status_code == 204

            assert_response = requests.get(url)

            assert assert_response.status_code == 204

        _()
        
        def _must_return_404_not_found_when_id_not_exists():
            
            url = self._get_view_url() + f'/{self.fake_id}'

            response = requests.delete(url)

            assert response.status_code == 404

            item = response.json()

            assert item['status_code'] == 404
            assert item['message'] == OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self.fake_id)

        _must_return_404_not_found_when_id_not_exists()

    def encode(self, db_model):
        return ViewEncoder().default(db_model)

    def _get_view_url(self):
        base_url = get_base_url()



        return f'{base_url}/{self.view_name}'








