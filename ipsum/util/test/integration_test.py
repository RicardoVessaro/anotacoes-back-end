
from collections import namedtuple
import functools
import requests

from ipsum.view.ipsum_view import ID

class IntegrationTest:
    
    def __init__(self):
        self._rest_data = namedtuple('RestData', 'base_url body')
        self._rest_id = namedtuple('RestId', 'base_url id')

        self.data = []
        self.ids = []

    def add_data(self, base_url:str, body):
        if type(body) is list:
            for b in body:
                self.data.append(self._rest_data(base_url, b))

        else:
            self.data.append(self._rest_data(base_url, body))

    def test(self):

        def decorate(func):

            @functools.wraps(func)
            def _test(*args, **kwargs):

                self._insert()

                try:
                    func(*args, **kwargs)

                except Exception as e:
                    raise e
                    
                finally:
                    self._delete()

            return _test

        return decorate

    def _insert(self):
        for data in self.data:
            response = requests.post(data.base_url, json=data.body)

            id = response.json()[ID]
            data.body[ID] = id

            self.ids.append(self._rest_id(data.base_url, id))

    def _delete(self):
        for id in self.ids:
            delete_url = f'{id.base_url}/{id.id}'
            
            requests.delete(delete_url)

        self.ids = []
