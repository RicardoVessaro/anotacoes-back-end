
from abc import abstractproperty, abstractmethod

import requests
from ipsum.exception.exception_message import CHILD_NOT_FOUND_IN_PARENT, PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.util.service.collection_tree import CollectionTree
from ipsum.util.test.database_test import DatabaseTest
from ipsum.util.test.view.ipsum_view_test import ID_FIELD, TO_MONGO_ID_FIELD
from ipsum.util.test.view.crud_view_test import CRUDViewTest
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.util.view.route_parser import parse_route
from bson import ObjectId

class DetailCRUDViewTest(CRUDViewTest):

    fake_parent_id = '627ffd74ee52c2e97a757b86'

    _params = None

    @property
    def collection_tree(self) -> CollectionTree:
        return self.service.collection_tree

    @property
    def ROUTE_PREFIX(self):
        if self._params is None:
            params = {}

            for item in self.collection_tree:
                if self.collection_tree.is_parent(item):
                    params[item.field] = self.fake_parent_id

                elif self.collection_tree.is_child(item):
                    pass

                else:
                    params[item.field] = str(ObjectId())

            self._params = params

        return parse_route(self.view.route_prefix, self._params)

    @property
    def parent_field(self):
        return self.model.parent_field

    @property
    def parent(self):
        return self.collection_tree.parent

    @property
    def parent_name(self):
        return self.parent.name

    @property
    def parent_dao(self):
        return self.parent.dao
    
    @abstractmethod
    def get_parent_model(self):
        pass

    def test_validate_collection_tree_must_raise_exception_when_parent_not_exists(self):
        url = self.get_view_url() + '/'

        db_model = self.get_model()

        data = self.encode(db_model)

        response = requests.post(url, json=data)

        response_data = response.json()

        error_message = PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE.format(self.parent_field, data[self.parent_field])
        assert response_data["status_code"] == IpsumException.BAD_REQUEST
        assert response_data['message'] == error_message

    def test_validate_collection_tree_must_raise_exception_when_child_not_in_parent(self):
        other_parent_id = '628ea6bf1db1dae1666aa849'

        database_test = DatabaseTest(host=self.INTEGRATION_TEST_DB_URI, daos_to_clean=[self.parent_dao, self.dao], parent_ids_to_clean=[other_parent_id])

        fake_parent_dict = self.get_parent_model().to_mongo()
        fake_parent_dict.pop(TO_MONGO_ID_FIELD)
        fake_parent_dict[ID_FIELD] = other_parent_id
        fake_parent = self.parent_dao.model(**fake_parent_dict)
        self._add_data(database_test, self.parent_dao, fake_parent)

        db_model = self.get_model()
        db_model[self.parent_field] = other_parent_id
        self._add_data(database_test, self.dao, db_model)
    
        @database_test.persistence_test()
        def _():
            id = str(db_model.id)
            url = self.get_view_url() + f'/{id}'

            updated_model = self.get_updated_model()
            updated_model.id = db_model.id

            data = self.encode(updated_model)

            response = requests.patch(url, json=data)

            response_data = response.json()
            error_message = CHILD_NOT_FOUND_IN_PARENT.format(
                self.view_name,
                id,
                self.parent_field,
                other_parent_id,
                self.parent_name,
                self.fake_parent_id
            )
            assert response_data["status_code"] == IpsumException.BAD_REQUEST
            assert response_data["message"] == error_message

            
