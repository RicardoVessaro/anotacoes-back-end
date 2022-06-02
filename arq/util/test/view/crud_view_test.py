
from abc import abstractproperty
import requests
from arq.exception.arq_exception import ArqException
from arq.util.object_util import is_none_or_empty

from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import ArqViewTest
from arq.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE, REQUIRED_FIELD_EXCEPTION_MESSAGE

class CRUDViewTest(ArqViewTest):

    def test_insert(self):

        if self._is_detail_crud_dao(self.dao):
            database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.dao], parent_ids_to_clean=[self.fake_parent_id])
            self._add_parent_data(database_test)

        else :
            database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.dao])

        @database_test.persistence_test()
        def _():
            url = self.get_view_url() + '/'

            db_model = self.get_model()

            data = self.encode(db_model)

            response = requests.post(url, json=data)

            item = response.json()

            for k in data:
                assert data[k] == item[k]

        _()

    def test_validate_required_fields_on_insert(self):

        if self._is_detail_crud_dao(self.dao):
            database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.dao], parent_ids_to_clean=[self.fake_parent_id])
            self._add_parent_data(database_test)

        else :
            database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.dao])

        @database_test.persistence_test()
        def _():

            for required_field in self.service.validator.required_fields:
                if is_none_or_empty(self.fields_inserted_by_default) or required_field not in self.fields_inserted_by_default:
                    url = self.get_view_url() + '/'

                    db_model = self.get_model()

                    data = self.encode(db_model)
                    
                    data.pop(required_field)

                    response = requests.post(url, json=data)

                    response_data = response.json()

                    error_message = REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)
                    assert response_data["status_code"] == ArqException.BAD_REQUEST
                    assert response_data["message"] == error_message
        _()

    def test_validate_required_fields_on_update(self):
        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)

        db_model = self.get_model()

        self._insert_parent(database_test)

        self._add_data(database_test, self.dao, db_model)
    
        @database_test.persistence_test()
        def _():
            for required_field in self.service.validator.required_fields:
                if is_none_or_empty(self.fields_inserted_by_default) or required_field not in self.fields_inserted_by_default:
                    
                    id = str(db_model.id)
                    url = self.get_view_url() + f'/{id}'

                    updated_model = self.get_updated_model()
                    updated_model.id = db_model.id

                    data = self.encode(updated_model)
                    data[required_field] = None

                    response = requests.patch(url, json=data)
                    response_data = response.json()

                    error_message = REQUIRED_FIELD_EXCEPTION_MESSAGE.format(required_field)
                    assert response_data["status_code"] == ArqException.BAD_REQUEST
                    assert response_data["message"] == error_message

        _()


    def test_update(self):
        
        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)

        db_model = self.get_model()

        self._insert_parent(database_test)

        self._add_data(database_test, self.dao, db_model)
    
        @database_test.persistence_test()
        def _():
            def update_sucess():
                id = str(db_model.id)
                url = self.get_view_url() + f'/{id}'

                updated_model = self.get_updated_model()
                updated_model.id = db_model.id

                data = self.encode(updated_model)

                response = requests.patch(url, json=data)

                item = response.json()

                for k in data:
                    assert data[k] == item[k]

            update_sucess()

            def _must_return_404_not_found_when_id_not_exists():
                url = self.get_view_url() + f'/{self.fake_id}'

                updated_model = self.get_updated_model()
                updated_model.id = db_model.id

                data = self.encode(updated_model)

                response = requests.patch(url, json=data)

                assert response.status_code == 404

                item = response.json()

                assert item['status_code'] == 404
                assert item['message'] == OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self.fake_id)

            _must_return_404_not_found_when_id_not_exists()

        _()

    def test_delete(self):
        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)

        db_model = self.get_model()
        self._add_data(database_test, self.dao, db_model)
    
        @database_test.persistence_test()
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

    def _insert_parent(self, database_test):
        if self._is_detail_crud_dao(self.dao):
            self._add_parent_data(database_test)
