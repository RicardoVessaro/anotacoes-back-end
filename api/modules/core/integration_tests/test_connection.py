import os
import requests

from arq.util.test.integration_test import get_base_url

def test_assert_is_test_enviroment():
        def is_test_enviroment():
            TEST_ENVIROMENT = 'TEST_ENVIROMENT'

            if TEST_ENVIROMENT in os.environ:
                return str(os.environ[TEST_ENVIROMENT]) == '1'

        # TODO Usar URI por variavel de ambiente
        #assert is_test_enviroment == True

def test_connection():

    base_url = get_base_url()

    requests.get(base_url)