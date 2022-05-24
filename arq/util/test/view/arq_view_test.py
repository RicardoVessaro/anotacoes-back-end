
import pytest
import requests

from collections import namedtuple
from abc import ABC, abstractproperty, abstractmethod
from arq.exception.exception_message import PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from arq.util.enviroment_variable import get_api_url
from arq.util.object_util import is_none_or_empty
from arq.util.test.database_test import DatabaseTest, clean_enums, insert_enums
from arq.util.view.view_encoder import ViewEncoder
from mongoengine import connect, disconnect

ID_FIELD = 'id'

FindFilterResult = namedtuple('FindFilterResult', 'filter expected_indexes')

PaginateFilterResult = namedtuple('PaginateFilterResult', 'filter expected_indexes pages page limit total has_prev has_next has_result')

class ArqViewTest(ABC):

    fake_id = '6248620366564103f229595f'

    is_enum = False

    enum_service = None

    @abstractproperty
    def ROUTE_PREFIX(self):
        pass

    @abstractproperty
    def enum_services_to_insert(self):
        pass

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

    @abstractproperty
    def find_filter_results(self):
        pass

    @abstractproperty
    def paginate_filter_results(self):
        pass

    @abstractproperty
    def filter_to_not_found(self):
        pass

    @abstractmethod
    def find_model_list(self):
        pass

    @abstractmethod
    def paginate_model_list(self):
        pass
    
    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def get_updated_model(self):
        pass

    @pytest.fixture(scope="class", autouse=True)
    def insert_enums(self):
        insert_enums(self.INTEGRATION_TEST_DB_URI, self.enum_services_to_insert)

        yield 

        clean_enums(self.INTEGRATION_TEST_DB_URI, self.enum_services_to_insert)

        if self.is_enum and not self.enum_service is None:
            connect(host=self.INTEGRATION_TEST_DB_URI)

            self.enum_service.save_enums()

            disconnect()

    def test_find_by_id(self):

        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)

        db_model = self.get_model()
        database_test.add_data(self.dao, db_model)
    
        @database_test.persistence_test()
        def _():
            id = str(db_model.id)
            url = self.get_view_url() + f'/{id}'

            response = requests.get(url)

            item = response.json()

            dict_model = self.encode(db_model)

            for k in item:
                assert item[k] == dict_model[k]
        _()

        def _must_return_204_no_content_when_id_not_exists():

            url = self.get_view_url() + f'/{self.fake_id}'

            response = requests.get(url)

            assert response.status_code == 204

        _must_return_204_no_content_when_id_not_exists()

    def test_find(self):

        model_list = self.find_model_list()

        url = self.get_view_url()

        arq_database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)
        arq_database_test.add_data(self.dao, model_list)

        @arq_database_test.persistence_test()
        def _():

            def test_POST():
                
                for find_filter_result in self.find_filter_results:
                    
                    response = requests.post(url, json=find_filter_result.filter)

                    expected_ids = self.get_expected_ids(find_filter_result.expected_indexes, model_list)

                    items = response.json()

                    assert len(items) == len(expected_ids)

                    for item in items:
                        assert item['id'] in expected_ids         
            
            test_POST()

            def test_GET():
                
                for find_filter_result in self.find_filter_results:
                    
                    response = requests.get(url, params=find_filter_result.filter)

                    expected_ids = self.get_expected_ids(find_filter_result.expected_indexes, model_list)

                    items = response.json()

                    assert len(items) == len(expected_ids)

                    for item in items:
                        assert item['id'] in expected_ids         
            
            test_GET()
            
        _()

    def test_paginate(self):

        model_list = self.paginate_model_list()

        url = self.get_view_url() + '/paginate'

        arq_database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)
        arq_database_test.add_data(self.dao, model_list)

        @arq_database_test.persistence_test()
        def _():
            
            for paginate_filter_result in self.paginate_filter_results:
                response = requests.post(url, json=paginate_filter_result.filter)

                items = response.json()

                assert items['pages'] == paginate_filter_result.pages
                assert items['page'] == paginate_filter_result.page
                assert items['limit'] == paginate_filter_result.limit
                assert items['total'] == paginate_filter_result.total
                assert items['has_prev'] == paginate_filter_result.has_prev
                assert items['has_next'] == paginate_filter_result.has_next
                assert items['has_result'] == paginate_filter_result.has_result

                expected_ids = self.get_expected_ids(paginate_filter_result.expected_indexes, model_list)

                pagination_item = items['items']

                assert len(pagination_item) == len(expected_ids)

                for item in pagination_item:
                    assert item['id'] in expected_ids  

            def _test_must_return_400_bad_reqeuest_when_page_is_higher_than_max_pages():
                model_list_length = len(model_list)
                page = str(model_list_length + 1)

                response = requests.post(url, json={"limit":1, "page": page })

                assert response.status_code == 400

                items = response.json()

                assert items['message'] == PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(page, model_list_length)
                assert items['status_code'] == 400

            _test_must_return_400_bad_reqeuest_when_page_is_higher_than_max_pages()

            def _test_must_return_empty_when_not_found_in_filter():
                response = requests.post(url, json=self.filter_to_not_found)

                items = response.json()

                assert items['pages'] == 0
                assert items['page'] == 0
                assert items['limit'] == 0
                assert items['total'] == 0
                assert items['has_prev'] == False
                assert items['has_next'] == False
                assert items['has_result'] == False
                assert is_none_or_empty(items['items']) 

            _test_must_return_empty_when_not_found_in_filter()
            
        _()


    def encode(self, db_model):
        return ViewEncoder().default(db_model)

    def get_view_url(self, with_view_name=True):
        base_url = get_api_url()

        view_url = f'{base_url}/{self.ROUTE_PREFIX}'

        if with_view_name:
            view_url += f'{self.view_name}'
        
        return view_url

    def get_expected_ids(self, expected_indexes, model_list):
        expected_ids = []

        for i in expected_indexes:
            find_model = model_list[i]

            expected_ids.append(str(find_model.id))
        
        return expected_ids










