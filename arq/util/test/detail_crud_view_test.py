
from abc import abstractproperty, abstractmethod
from arq.util.test.view.crud_view_test import CRUDViewTest


class DetailCRUDViewTest(CRUDViewTest):

    @abstractproperty
    def fake_parent_id(self):
        pass

    @abstractproperty
    def parent_field(self):
        pass

    @abstractproperty
    def parent_dao(self):
        pass
    
    @abstractmethod
    def get_parent_model(self):
        pass


