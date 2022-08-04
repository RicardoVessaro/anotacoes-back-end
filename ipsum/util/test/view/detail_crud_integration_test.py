
from abc import abstractproperty
from collections import namedtuple
from copy import copy

from ipsum.util.enviroment_variable import get_api_url
from ipsum.util.object_util import is_none_or_empty
from ipsum.util.test.integration_test import IntegrationTest
from ipsum.util.test.view.crud_integration_test import CRUDIntegrationTest
from ipsum.view.ipsum_view import ID

DependencyParent = namedtuple('DependencyParent', 'url body')

class DetailCRUDIntegrationTest(CRUDIntegrationTest):

    @abstractproperty
    def parent_base_url(self):
        pass

    @abstractproperty
    def parent_field(self):
        pass

    @abstractproperty
    def parent_body(self):
        pass

    dependency_parents = []

    def test_insert(self):
        integration_test = IntegrationTest()
        self.prepare_dependency_parents(integration_test)
        integration_test.add_data(self.parent_url(), self.parent_body)

        @integration_test.test()
        def _():
            self.assert_insert()
        _()
    
    def test_update(self):

        integration_test = self.prepare_integration_test()

        @integration_test.test()
        def _():
            self._must_update()
        _()

        integration_test = IntegrationTest()
        self.prepare_dependency_parents(integration_test)
        integration_test.add_data(self.parent_url(), self.parent_body)
        
        @integration_test.test()
        def _():
            self._must_return_404_not_found_when_id_not_exists()
        _()

    def prepare_integration_test(self, body_list=[]):
        integration_test = IntegrationTest()

        self.prepare_dependency_parents(integration_test)

        if is_none_or_empty(body_list):

            integration_test.add_data(self.parent_url(), self.parent_body)
            integration_test.add_data(self.url(), self.body)
        
        else:

            inserted_parent_ids = []

            for body in body_list: 
                parent_id = self.body[self.parent_field]

                body_parent_id = body[self.parent_field]

                body_url = self.url().replace(parent_id, body_parent_id)
                if parent_id != body_parent_id:

                    body_parent = copy(self.parent_body)
                    body_parent[ID] = body_parent_id

                    integration_test.add_data(self.parent_url(), body_parent)
                    inserted_parent_ids.append(body_parent_id)

                else:
                    integration_test.add_data(self.parent_url(), self.parent_body)

                integration_test.add_data(body_url, body)
        

        return integration_test

    def prepare_dependency_parents(self, integration_test):
        if not is_none_or_empty(self.dependency_parents):
            for dependency_parent in self.dependency_parents:
                integration_test.add_data(
                    dependency_parent.url, dependency_parent.body)

    def parent_url(self):
        return f'{get_api_url()}/{self.parent_base_url}'

    def _get_body_list_length(self, body_list):
        body_list_length = 0

        for body in body_list:
            if str(body[self.parent_field]) == self.body[self.parent_field]:
                body_list_length += 1

        return body_list_length

    