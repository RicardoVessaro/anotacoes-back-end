
import functools
from mongoengine import connect, disconnect
from collections import namedtuple
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO

from ipsum.util.object_util import is_none_or_empty

def insert_enums(host, enum_services_to_insert):
    connect(host=host)

    _insert_enums(enum_services_to_insert)

    disconnect()

def clean_enums(host, enum_services_to_insert):
    connect(host=host)

    _clean_enums(enum_services_to_insert)

    disconnect()

def _insert_enums(enum_services_to_insert):
    _clean_enums(enum_services_to_insert)
    
    if not is_none_or_empty(enum_services_to_insert):
        for enum_service in enum_services_to_insert:
            enum_service.save_enums()

def _clean_enums(enum_services_to_insert):
    if not is_none_or_empty(enum_services_to_insert):
        for enum_service in enum_services_to_insert:
            _delete_dao_data(enum_service._dao)

def _delete_dao_data(dao, parent_ids=None):
    data_to_delete_list = []

    if is_none_or_empty(parent_ids):
        data_to_delete_list = dao.find()
    else:
        for parent_id in parent_ids:
            data_to_delete_list.extend(dao.find(parent_id))

    for data_to_delete in data_to_delete_list:
        dao.delete(data_to_delete.id)

class DatabaseTest:

    def __init__(self, host, daos_to_clean=[], parent_ids_to_clean=[], enum_services_to_insert=[]) -> None:
        self.host = host
        self.data_to_insert = []
        self._data = namedtuple('Data', ['dao', 'model', 'data_id', 'parent_ids'])
        self.daos_to_clean = daos_to_clean
        self.parent_ids_to_clean = parent_ids_to_clean
        self.enum_services_to_insert = enum_services_to_insert

    def add_data(self, dao, model, parent_ids=[]):
        if type(model) is list:
            for m in model:
                data = self._data(dao=dao, model=m, data_id=None, parent_ids=parent_ids)
                self.data_to_insert.append(data)
            
        else:
            data = self._data(dao=dao, model=model, data_id=None, parent_ids=parent_ids)
            self.data_to_insert.append(data)

    def persistence_test(self, clean_database=True):

        def decorate(func):

            @functools.wraps(func)
            def test(*args, **kwargs):
                self._connect()

                if clean_database:
                    self._clean_existing_data()
                
                _insert_enums(self.enum_services_to_insert)

                self._insert_data()

                try:
                    func(*args, **kwargs)

                except Exception as e:
                    self._delete_data()
                    _clean_enums(self.enum_services_to_insert)

                    raise e
                    
                finally:
                    if clean_database:
                        self._delete_data()
                        _clean_enums(self.enum_services_to_insert)

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
            inserted_data.append(self._data(dao=data.dao, model=data.model, data_id=data_id, parent_ids=data.parent_ids))

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
                self._delete_dao_data(dao, data.parent_ids)

                already_deleted.append(dao)

        for dao in self.daos_to_clean:
            if isinstance(dao, DetailCRUDDAO):
                self._delete_dao_data(dao, self.parent_ids_to_clean)
                    
            else:
                self._delete_dao_data(dao)

            already_deleted.append(dao)

    def _delete_dao_data(self, dao, parent_ids=None):
        _delete_dao_data(dao, parent_ids)

    def _connect(self):
        connect(host=self.host)

    def _disconnect(self):
        disconnect()