
import pytest
import requests

from collections import namedtuple
from abc import ABC, abstractproperty, abstractmethod
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.exception.exception_message import PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.service.enum.enum_service import EnumService
from ipsum.util.enviroment_variable import get_api_url, get_test_database_url
from ipsum.util.object_util import is_none_or_empty
from ipsum.util.test.database_test import DatabaseTest, clean_enums, insert_enums
from ipsum.util.view.view_encoder import ViewEncoder
from mongoengine import connect, disconnect

ID_FIELD = 'id'
TO_MONGO_ID_FIELD = '_id'
HATEOAS_LINKS = '_links'

PaginateFilterResult = namedtuple('PaginateFilterResult', 'filter expected_indexes pages page limit total has_prev has_next has_result')

class IpsumViewTest(ABC):

    fake_id = '6248620366564103f229595f'

    @abstractproperty
    def view(self):
        pass

    @abstractproperty
    def paginate_filter_results(self):
        pass

    @property
    def ROUTE_PREFIX(self):
        return self.view.route_prefix

    @property
    def service(self):
        return self.view.service

    @property
    def is_enum(self):
        return isinstance(self.service, EnumService)

    @property
    def fields_inserted_by_default(self):
        return self.service.fields_inserted_by_default

    @property
    def INTEGRATION_TEST_DB_URI(self):
        return get_test_database_url()

    @property        
    def view_name(self):
        return self.view.get_route_base()

    @property
    def dao(self):
        return self.service.dao

    @property
    def model(self):
        return self.dao.model

    @abstractproperty
    def filter_to_not_found(self):
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
        yield 

        if self.is_enum:
            connect(host=self.INTEGRATION_TEST_DB_URI)

            self.service.save_enums()

            disconnect()

    def test_find_by_id(self):

        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)

        db_model = self.get_model()
        self._add_data(database_test, self.dao, db_model)

        @database_test.persistence_test()
        def _():
            id = str(db_model.id)
            url = self.get_view_url() + f'/{id}'

            response = requests.get(url)

            item = response.json()

            dict_model = self.encode(db_model)

            for k in item:
                if k != HATEOAS_LINKS:
                    assert item[k] == dict_model[k]
        _()

        def _must_return_204_no_content_when_id_not_exists():

            url = self.get_view_url() + f'/{self.fake_id}'

            response = requests.get(url)

            assert response.status_code == 204

        _must_return_204_no_content_when_id_not_exists()

    def test_find(self):

        model_list = self.paginate_model_list()

        url = self.get_view_url()

        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI)
        self._add_data(database_test, self.dao, model_list)

        if self._is_detail_crud_dao(self.dao):
            self._add_parent_data(database_test)

        @database_test.persistence_test()
        def _():
            
            for paginate_filter_result in self.paginate_filter_results:
                response = requests.get(url, params=paginate_filter_result.filter)

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
                model_list_length = self._get_model_list_length(model_list)

                page = str(model_list_length + 1)

                response = requests.get(url, params={"limit":1, "page": page })

                assert response.status_code == 400

                items = response.json()

                assert items['message'] == PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(page, model_list_length)
                assert items['status_code'] == 400

            _test_must_return_400_bad_reqeuest_when_page_is_higher_than_max_pages()

            def _test_must_return_empty_when_not_found_in_filter():
                response = requests.get(url, params=self.filter_to_not_found)

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

    def _add_parent_data(self, database_test):
        self._add_data(database_test, self.parent_dao, self.get_parent_model())

    def _add_data(self, database_test, dao, db_model):

        if self._is_detail_crud_dao(dao):
            database_test.add_data(dao, db_model, [self.fake_parent_id])

        else:
            database_test.add_data(dao, db_model)

    def _get_model_list_length(self, model_list):
        model_list_length = len(model_list)

        if self._is_detail_crud_dao(self.dao):
            count_by_parent_id = 0

            for model in model_list:
                if str(model[self.parent_field]) == self.fake_parent_id:
                    count_by_parent_id += 1

            model_list_length = count_by_parent_id

        return model_list_length

    def _is_detail_crud_dao(self, dao):
        return isinstance(dao, DetailCRUDDAO)








