
from abc import abstractproperty
from copy import copy
import requests
from ipsum.exception.exception_message import OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.util.object_util import is_none_or_empty
from ipsum.util.test.integration_test import IntegrationTest
from ipsum.util.test.view.view_integration_test import ViewIntegrationTest
from ipsum.view.ipsum_view import ID, STATUS_CREATED, STATUS_NO_CONTENT, STATUS_NOT_FOUND, STATUS_OK


class CRUDIntegrationTest(ViewIntegrationTest):

    @abstractproperty
    def body(self):
        pass

    @abstractproperty
    def update_body(self):
        pass

    def url_with_id(self):
        return f'{self.url()}/{self.body[ID]}'

    def test_find_by_id(self):
        
        integration_test = self.prepare_integration_test()

        @integration_test.test()
        def _():

            def _must_find_by_id():
                response = requests.get(self.url_with_id())
                
                self.print_error(response)

                assert response.status_code == STATUS_OK

                body = response.json()
                assert body[ID] == self.body[ID]

            _must_find_by_id()

            def _must_return_no_content_when_id_not_exists():
                not_inserted_id = '62b35377d0f769338f8ae117'
                url = f'{self.url()}/{not_inserted_id}'
                
                response = requests.get(url)

                self.print_error(response)

                assert response.status_code == STATUS_NO_CONTENT

            _must_return_no_content_when_id_not_exists()
        _()

    def test_find(self):

        body_list = self.body_list()

        integration_test = self.prepare_integration_test(body_list)

        @integration_test.test()
        def _():
            self.assert_find(body_list)
        _()
    
    def test_insert(self):
        self.assert_insert()

    def assert_insert(self):
        body = copy(self.body)
        body[ID] = '629fd999bcb136d8e94981ae'

        response = requests.post(self.url(), json=body)

        self.print_error(response)

        assert response.status_code == STATUS_CREATED

        self.print_error(response)

        response_body = response.json()

        for field in body:
            assert body[field] == response_body[field]

        url = f'{self.url()}/{body[ID]}'
        requests.delete(url)

    def test_update(self):

        integration_test = self.prepare_integration_test()

        @integration_test.test()
        def _():
            self._must_update()
        _()

        self._must_return_404_not_found_when_id_not_exists()

    def _must_update(self):
            
        response = requests.patch(self.url_with_id(), json=self.update_body)

        self.print_error(response)

        assert response.status_code == STATUS_OK

        response = requests.get(self.url_with_id())
        body = response.json()

        for field in self.update_body:
            assert self.update_body[field] == body[field]

    def _must_return_404_not_found_when_id_not_exists(self):
        response = requests.patch(self.url_with_id(), json=self.update_body)

        self.print_error(response)

        assert response.status_code == STATUS_NOT_FOUND

        item = response.json()

        assert item['status_code'] == STATUS_NOT_FOUND
        assert item['message'] == OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self.body[ID])

    def test_delete(self):
        
        integration_test = self.prepare_integration_test()

        @integration_test.test()
        def _():

            response = requests.delete(self.url_with_id())
            response.status_code == STATUS_NO_CONTENT

            response = requests.get(self.url_with_id())
            assert response.status_code == STATUS_NO_CONTENT

        _()

    def prepare_integration_test(self, body_list=[]):
        integration_test = IntegrationTest()

        if is_none_or_empty(body_list):
            integration_test.add_data(self.url(), self.body)
        
        else:
            integration_test.add_data(self.url(), body_list)

        return integration_test
