
import functools
from mongoengine import connect, disconnect
from collections import namedtuple
from ipsum.data.dao.dao import ID, _ID
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO

from ipsum.util.object_util import is_none_or_empty

class DatabaseTest:

    def __init__(self, daos_to_clean=[], parent_ids_to_clean=[], enum_services_to_insert=[]) -> None:
        self._host = 'mongomock://localhost'
        self.data_to_insert = []
        self._data = namedtuple('Data', ['dao', 'model', 'data_id', 'parent_ids'])
        self.daos_to_clean = daos_to_clean
        self.parent_ids_to_clean = parent_ids_to_clean
        self.enum_services_to_insert = enum_services_to_insert

    @property
    def host(self):
        return self._host

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
                
                self._insert_enums()

                self._insert_data()

                try:
                    func(*args, **kwargs)

                except Exception as e:
                    self._delete_data()
                    self._clean_enums()

                    raise e
                    
                finally:
                    if clean_database:
                        self._delete_data()
                        self._clean_enums()

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
        cleaned_data_to_insert = []

        for data in self.data_to_insert:
            dao = data.dao

            if data.data_id is not None and dao.find_by_id(data.data_id) is not None:
                dao.delete(data.data_id)

            new_data = self._refresh_data(data)

            cleaned_data_to_insert.append(new_data)

        self.data_to_insert = cleaned_data_to_insert

    def _refresh_data(self, data):
        model_data = data.model
        model_data = model_data.to_mongo()
        model_data[ID] = model_data.pop(_ID)
        model_data = data.dao.model(**model_data)

        return self._data(dao=data.dao, model=model_data, data_id=None, parent_ids=data.parent_ids)
    
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
        self._delete_dao_data(dao, parent_ids)

    def _insert_enums(self):
        self._clean_enums()
        
        if not is_none_or_empty(self.enum_services_to_insert):
            for enum_service in self.enum_services_to_insert:
                enum_service.save_enums()

    def _clean_enums(self):
        if not is_none_or_empty(self.enum_services_to_insert):
            for enum_service in self.enum_services_to_insert:
                self._delete_dao_data(enum_service._dao)

    def _delete_dao_data(self, dao, parent_ids=None):
        data_to_delete_list = []

        if is_none_or_empty(parent_ids):
            data_to_delete_list = dao.find()
        else:
            for parent_id in parent_ids:
                data_to_delete_list.extend(dao.find(parent_id))

        for data_to_delete in data_to_delete_list:
            dao.delete(data_to_delete.id)

    def _connect(self):
        connect(host=self.host)

    def _disconnect(self):
        disconnect()
