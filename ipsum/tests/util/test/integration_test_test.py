
from unittest.mock import Mock, call, patch

from pytest import raises
from ipsum.util.test.integration_test import IntegrationTest
from ipsum.util.test.integration_test import requests
from ipsum.view.ipsum_view import ID


class TestIntegrationTest:

    def test_add_data(self):

        integration_test = IntegrationTest()

        BASE_URL = 'base-url'
        data_1 = {'code': 1, 'name': 'test 1'}
        data_2 = {'code': 2, 'name': 'test 2'}

        integration_test.add_data(
            base_url=BASE_URL,
            body=data_1
        )

        integration_test.add_data(
            base_url=BASE_URL,
            body=data_2
        )

        assert len(integration_test.data) == 2

        test_data = integration_test.data[0]
        assert test_data.base_url == BASE_URL
        assert test_data.body == data_1

        test_data = integration_test.data[1]
        assert test_data.base_url == BASE_URL
        assert test_data.body == data_2

    def test_add_data_list(self):

        integration_test = IntegrationTest()

        BASE_URL = 'base-url'
        data_1 = {'code': 1, 'name': 'test 1'}
        data_2 = {'code': 2, 'name': 'test 2'}

        integration_test.add_data(
            base_url=BASE_URL,
            body=[data_1, data_2]
        )

        assert len(integration_test.data) == 2

        test_data = integration_test.data[0]
        assert test_data.base_url == BASE_URL
        assert test_data.body == data_1

        test_data = integration_test.data[1]
        assert test_data.base_url == BASE_URL
        assert test_data.body == data_2
        
    @patch.object(requests, 'post')
    def test_insert(self, post_mock):
        BASE_URL = 'base-url'
        data_1 = {'code': 1, 'name': 'test 1'}
        data_2 = {'code': 2, 'name': 'test 2'}

        integration_test = IntegrationTest()

        integration_test.add_data(
            base_url=BASE_URL,
            body=data_1
        )

        integration_test.add_data(
            base_url=BASE_URL,
            body=data_2
        )

        id_1 = '1'
        id_2 = '2'

        post_mock.side_effect = [self._ResponseMock(id_1), self._ResponseMock(id_2)]

        integration_test._insert()

        assert ID in data_1
        assert not data_1[ID] is None
        data_1.pop(ID)

        assert ID in data_2
        assert not data_2[ID] is None
        data_2.pop(ID)

        assert post_mock.mock_calls == [
            call(BASE_URL, json=data_1), 
            call(BASE_URL, json=data_2)
        ]

        assert len(integration_test.ids) == 2

        test_id = integration_test.ids[0]
        assert test_id.base_url == BASE_URL
        assert test_id.id == id_1

        test_id = integration_test.ids[1]
        assert test_id.base_url == BASE_URL
        assert test_id.id == id_2

    @patch.object(requests, 'delete')
    @patch.object(requests, 'post')
    def test_delete(self, post_mock, delete_mock):

        BASE_URL = 'base-url'
        data_1 = {'code': 1, 'name': 'test 1'}
        data_2 = {'code': 2, 'name': 'test 2'}

        integration_test = IntegrationTest()

        integration_test.add_data(
            base_url=BASE_URL,
            body=data_1
        )

        integration_test.add_data(
            base_url=BASE_URL,
            body=data_2
        )

        id_1 = '1'
        id_2 = '2'

        post_mock.side_effect = [self._ResponseMock(id_1), self._ResponseMock(id_2)]

        integration_test._insert()

        integration_test._delete()

        DELETE_URL = BASE_URL+'/'+'{0}'

        assert integration_test.ids == []

        assert delete_mock.mock_calls == [
            call(DELETE_URL.format(id_1),), 
            call(DELETE_URL.format(id_2),)
        ]

    def test_test_decorator(self):

        integration_test = IntegrationTest()

        integration_test._insert = Mock()
        integration_test._delete = Mock()

        @integration_test.test()
        def function():
            pass

        function()
        
        integration_test._insert.assert_called_once()
        integration_test._delete.assert_called_once()

    def test_test_decorator_call_delete_when_an_exception_occurs(self):

        integration_test = IntegrationTest()

        integration_test._insert = Mock()
        integration_test._delete = Mock()

        error_message = "Test Error"

        @integration_test.test()
        def function():
            raise Exception(error_message)

        with raises(Exception, match=error_message):    
            function()
            
        integration_test._insert.assert_called_once()
        integration_test._delete.assert_called_once()


    class _ResponseMock:

        def __init__(self, id) -> None:
            self.id = id

        def json(self):
            return {'id': self.id}
