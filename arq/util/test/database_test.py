
import functools
from mongoengine import connect, disconnect
from collections import namedtuple

from arq.util.object_util import is_none_or_empty

class DatabaseTest:

    def __init__(self, host, daos_to_clean=[], enum_services_to_insert=[]) -> None:
        self.host = host
        self.data_to_insert = []
        self._data = namedtuple('Data', ['dao', 'model', 'data_id'])
        self.daos_to_clean = daos_to_clean
        self.enum_services_to_insert = enum_services_to_insert

        self._already_inserted = False

    def add_data(self, dao, model):
        if type(model) is list:
            for m in model:
                data = self._data(dao=dao, model=m, data_id=None)
                self.data_to_insert.append(data)
            
        else:
            data = self._data(dao=dao, model=model, data_id=None)
            self.data_to_insert.append(data)

    def persistence_test(self, clean_database=True):

        def decorate(func):

            @functools.wraps(func)
            def test(*args, **kwargs):
                self._connect()

                if clean_database:
                    self._clean_existing_data()
                
                self._insert_enums()

                self._insert_data()

                try:
                    func(*args, **kwargs)

                except Exception as e:
                    self._delete_data()

                    raise e
                    
                finally:
                    if clean_database:
                        self._delete_data()

                    self._disconnect()

            return test

        return decorate

    def insert_enums(self):
        self._connect()

        self._insert_enums()

        self._disconnect()

    def _insert_enums(self):
        if not is_none_or_empty(self.enum_services_to_insert) and not self._already_inserted:
            for enum_service in self.enum_services_to_insert:
                enum_service.save_enums()

            self._already_inserted = True

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

    def _connect(self):
        connect(host=self.host)

    def _disconnect(self):
        disconnect()