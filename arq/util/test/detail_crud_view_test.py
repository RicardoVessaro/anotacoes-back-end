
from abc import abstractproperty, abstractmethod

import requests
from arq.exception.exception_message import CHILD_NOT_FOUND_IN_PARENT, PARENT_OBJECT_NOT_FOUND_EXCEPTION_MESSAGE
from arq.util.test.database_test import DatabaseTest
from arq.util.test.view.arq_view_test import ID_FIELD, TO_MONGO_ID_FIELD
from arq.util.test.view.crud_view_test import CRUDViewTest
from arq.exception.arq_exception import ArqException

class DetailCRUDViewTest(CRUDViewTest):

    @abstractproperty
    def fake_parent_id(self):
        pass

    @abstractproperty
    def parent_field(self):
        pass

    @abstractproperty
    def parent_name(self):
        pass


    @abstractproperty
    def parent_dao(self):
        pass
    
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
        assert response_data["status_code"] == ArqException.BAD_REQUEST
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

            response = requests.put(url, json=data)

            response_data = response.json()
            error_message = CHILD_NOT_FOUND_IN_PARENT.format(
                self.view_name,
                id,
                self.parent_field,
                other_parent_id,
                self.parent_name,
                self.fake_parent_id
            )
            assert response_data["status_code"] == ArqException.BAD_REQUEST
            assert response_data["message"] == error_message

            
