
import functools
from mongoengine import connect, disconnect
from collections import namedtuple

# TODO criar teste unitario (dps que cirar teste com ModelTest)
class ArqDatabaseTest:

    def __init__(self) -> None:
        self.data_to_insert = []
        self._data = namedtuple('Data', ['dao', 'model', 'data_id'])

    def add_data(self, dao, model):
        data = self._data(dao=dao, model=model, data_id=None)
        self.data_to_insert.append(data)

    def persistence_test(self, host, clean_database=False):

        def decorate(func):

            @functools.wraps(func)
            def test(*args, **kwargs):
                self._connect(host)

                if clean_database:
                    self._clean_existing_data()

                self._insert_data()

                try:
                    func(*args, **kwargs)

                finally:
                    self._delete_data()

                    self._disconnect()

            return test

        return decorate

    def _insert_data(self):
        inserted_data = []
        for data in self.data_to_insert:
            dao = data.dao
            model = data.model

            dao.insert(model)

            data_id = model.id
            inserted_data.append(self._data(dao=data.dao, model=data.model, data_id=data_id))

        self.data_to_insert = inserted_data

    def _delete_data(self):
        for data in self.data_to_insert:
            dao = data.dao

            if dao.find_by_id(data.data_id) is not None:
                dao.delete(data.data_id)

    def _clean_existing_data(self):
        already_deleted = []

        for data in self.data_to_insert:
            dao = data.dao
            if dao not in already_deleted:
                data_to_delete_list = dao.find()

                for data_to_delete in data_to_delete_list:
                    dao.delete(data_to_delete.id)

                already_deleted.append(dao)

    def _connect(self, host):
        connect(host=host)

    def _disconnect(self):
        disconnect()