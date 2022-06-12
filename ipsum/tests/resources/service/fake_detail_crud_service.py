
from ipsum.service.detail_crud_service import DetailCRUDService
from ipsum.tests.resources.data.dao.fake_crud_dao import FakeCRUDDAO
from ipsum.tests.resources.data.dao.fake_detail_crud_dao import FakeDetailCRUDDAO
from ipsum.tests.resources.service.fake_detail_crud_validator import FakeDetailCRUDValidator
from ipsum.tests.resources.service.fake_crud_service import FakeCRUDService
from ipsum.util.service.collection_tree import CollectionItem, CollectionTree

class FakeDetailCRUDService(DetailCRUDService):

    NAME = 'fake-detail-crud-services'

    def __init__(self) -> None:
        dao = FakeDetailCRUDDAO()

        collection_tree = CollectionTree(
            parent=CollectionItem(
                name=FakeCRUDService.NAME,
                dao=FakeCRUDDAO(),
                parent_field=None,
                id=None,
                field=dao.model.parent_field
            ),
            child=CollectionItem(
                name=self.NAME,
                parent_field=dao.model.parent_field,
                dao=dao,
                id=None,
                field='id'
            )
        )

        validator = FakeDetailCRUDValidator(
            dao=collection_tree.child.dao,
            parent_dao=collection_tree.parent.dao
        )

        super().__init__(dao, validator, collection_tree)
