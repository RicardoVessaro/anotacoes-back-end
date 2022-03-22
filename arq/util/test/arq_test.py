
import functools
from mongoengine import connect, disconnect
from collections import namedtuple

# TODO criar teste unitario (dps que cirar teste com ModelTest)
class ArqDatabaseTest:

    def __init__(self, daos_to_clean=[]) -> None:
        self.data_to_insert = []
        self._data = namedtuple('Data', ['dao', 'model', 'data_id'])
        self.daos_to_clean = daos_to_clean

    def add_data(self, dao, model):
        if type(model) is list:
            for m in model:
                data = self._data(dao=dao, model=m, data_id=None)
                self.data_to_insert.append(data)
            
        else:
            data = self._data(dao=dao, model=model, data_id=None)
            self.data_to_insert.append(data)

    def persistence_test(self, host, clean_database=True):

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

        for dao in self.daos_to_clean:
            self._delete_dao_data(dao)

    def _clean_existing_data(self):
        already_deleted = []

        for data in self.data_to_insert:
            dao = data.dao
            if dao not in already_deleted:
                self._delete_dao_data(dao)

                already_deleted.append(dao)

        for dao in self.daos_to_clean:
            if dao not in already_deleted:
                self._delete_dao_data(dao)

                already_deleted.append(dao)

    def _delete_dao_data(self, dao):
        data_to_delete_list = dao.find()

        for data_to_delete in data_to_delete_list:
            dao.delete(data_to_delete.id)

    def _connect(self, host):
        connect(host=host)

    def _disconnect(self):
        disconnect()