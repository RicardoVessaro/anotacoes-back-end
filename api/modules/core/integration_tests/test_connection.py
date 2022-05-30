import requests
from mongoengine import connect, disconnect

from arq.util.enviroment_variable import get_api_url, get_test_database_url

def test_url_connection():

    base_url = get_api_url()

    requests.get(base_url)

def test_database_connection():
    
    test_database_url = get_test_database_url()

    connect(host=test_database_url)

    disconnect()
