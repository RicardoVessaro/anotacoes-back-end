import requests

from arq.util.enviroment_variable import get_api_url

def test_url_connection():

    base_url = get_api_url()

    requests.get(base_url)

def test_database_connection():
    pass
