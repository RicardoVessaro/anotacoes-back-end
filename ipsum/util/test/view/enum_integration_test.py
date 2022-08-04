
from abc import abstractproperty
import requests
from ipsum.data.model.enum_document import CODE, NAME
from ipsum.util.test.view.view_integration_test import ViewIntegrationTest
from ipsum.util.data.pagination import Pagination
from ipsum.util.view.hateoas_builder import HATEOASBuilder
from ipsum.view.ipsum_view import ID, STATUS_NO_CONTENT, STATUS_OK


class EnumIntegrationTest(ViewIntegrationTest):

    @abstractproperty
    def expected_enums(self):
        pass
    
    def body_list(self):

        pagination_url = f'{self.url()}?_limit={len(self.expected_enums)}'
        
        response = requests.get(pagination_url)

        body = response.json()

        enums = body[Pagination.ITEMS]

        for enum in enums:
            if HATEOASBuilder.HATEOAS_LINKS in enum:
                enum.pop(HATEOASBuilder.HATEOAS_LINKS)

        return enums

    def test_find_by_id(self):

        def _must_find_by_id():
            enum = self.body_list()[0]

            url = f'{self.url()}/{enum[ID]}'

            response = requests.get(url)

            assert response.status_code == STATUS_OK

            body = response.json()
            assert body[ID] == enum[ID]

        _must_find_by_id()

        def _must_return_no_content_when_id_not_exists():
            not_inserted_id = '62b35377d0f769338f8ae117'
            url = f'{self.url()}/{not_inserted_id}'
            
            response = requests.get(url)

            assert response.status_code == STATUS_NO_CONTENT

        _must_return_no_content_when_id_not_exists()

    def test_find(self):
        self.assert_find(self.body_list())

    def test_enums_saved(self):

        enums = self.body_list()

        for expected_enum in self.expected_enums:
            code_is_equal = False

            for enum in enums:
                code_is_equal = expected_enum[CODE] == enum[CODE]
            
                if code_is_equal:
                    assert expected_enum[NAME] == enum[NAME]
                    assert expected_enum[ID] == enum[ID]
                    break
            
            if not code_is_equal:
                print(expected_enum[CODE], enum[CODE])
            assert code_is_equal
