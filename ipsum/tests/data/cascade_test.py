
from pytest import raises
from bson import ObjectId
from ipsum.data.cascade import Cascade
from ipsum.data.dao.crud_dao import CRUDDAO
from ipsum.data.dao.dao import DAO
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.exception.exception_message import CASCADE_CHILDS_MUST_BE_INSTANCE_OF_DAO
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.tests.resources.data.model.detail_test_model import DetailTestModel
from ipsum.tests.resources.data.model.detail_child_test_model import DetailChildTestModel
from ipsum.util.enviroment_variable import get_test_database_url
from ipsum.util.test.database_test import DatabaseTest

class TestCascade:

    def test_validate_dao_type(self):
        class FakeModel:
            
            parent_field = 'parent_id'

        class FakeDAO(DetailCRUDDAO):
            
            def __init__(self) -> None:
                super().__init__(model=FakeModel)

        class NotDAO:
            pass
        
        with raises(IpsumException, match=CASCADE_CHILDS_MUST_BE_INSTANCE_OF_DAO.format(Cascade, Cascade.DAO_ATTRIBUTE, DetailCRUDDAO, NotDAO)):
            Cascade(childs=[
                FakeDAO(),
                DetailCRUDDAO(model=FakeModel),
                NotDAO()
            ])

    def test_simple_delete(self):

        class FakeDetailChildDAO(DetailCRUDDAO):

            def __init__(self) -> None:
                super().__init__(model=DetailChildTestModel)

        class FakeDetailDAO(DetailCRUDDAO):
            def __init__(self) -> None:
                super().__init__(
                    model=DetailTestModel,
                    cascade=Cascade(childs=[
                        FakeDetailChildDAO()
                    ])
                )

        class FakeParentDAO(DAO):
            def __init__(self) -> None:
                super().__init__(
                    model=IpsumTestModel, 
                    cascade=Cascade(childs=[
                        FakeDetailDAO()
                    ])
                )

        fake_parent_dao = FakeParentDAO()
        fake_detail_dao = FakeDetailDAO()

        id_fake_parent = ObjectId()
        fake_parent = fake_parent_dao.model(
            id=id_fake_parent,
            code=1
        )

        id_fake_detail = ObjectId()
        fake_detail = fake_detail_dao.model(
            id=id_fake_detail,
            code=11,
            ipsum_model_id=id_fake_parent
        )

        database_test = DatabaseTest(host=get_test_database_url())
        database_test.add_data(fake_parent_dao, fake_parent)
        database_test.add_data(fake_detail_dao, fake_detail, [id_fake_parent])

        @database_test.persistence_test()
        def _():
            
            fake_parent_dao.cascade.delete(fake_parent.id)

            assert not fake_parent_dao.find_by_id(fake_parent.id) is None
            assert fake_detail_dao.find_by_id(fake_detail.id) is None

        _()
        
        

    def test_delete(self):

        """
        Fake Tree dependencies:

            - fake_parent_dao
                - fake_detail_dao_1
                    - fake_detail_child_dao_1
                    - fake_detail_child_dao_2
                    
                - fake_detail_dao_2

        """

        class FakeDetailChildDAO1(DetailCRUDDAO):

            def __init__(self) -> None:
                super().__init__(model=DetailChildTestModel)

        class FakeDetailChildDAO2(DetailCRUDDAO):

            def __init__(self) -> None:
                super().__init__(model=DetailChildTestModel)

        class FakeDetailDAO1(DetailCRUDDAO):

            def __init__(self) -> None:
                super().__init__(
                    model=DetailTestModel, 
                    cascade=Cascade(childs=[
                        FakeDetailChildDAO1(),
                        FakeDetailChildDAO2()
                    ])
                )

        class FakeDetailDAO2(DetailCRUDDAO):

            def __init__(self) -> None:
                super().__init__(model=DetailTestModel)

        class FakeParentDAO(CRUDDAO):

            def __init__(self) -> None:
                super().__init__(
                    model=IpsumTestModel, 
                    cascade=Cascade(childs=[
                        FakeDetailDAO1(),
                        FakeDetailDAO2()
                    ])
                )

        fake_parent_dao = FakeParentDAO()
        
        fake_detail_dao_1 = FakeDetailDAO1()
        fake_detail_child_dao_1 = FakeDetailChildDAO1()
        fake_detail_child_dao_2 = FakeDetailChildDAO2()

        fake_detail_dao_2 = FakeDetailDAO2()
        

        """
        Setting data in database
        
        Pattern: - model_code (code)
        code :  
                (    x               x               x                   x                        x  )
                (   1/2             1/2             [1,2]               1/2                     [1,3])
                fake_parent - fake_detail - fake_detail_count - fake_detail_child - fake_detail_child_count

        - fake_parent_1 (1)
            - fake_detail_111 (111)
                - fake_detail_child_11111 (11111)
                - fake_detail_child_11112 (11112)
                - fake_detail_child_11113 (11113)

                - fake_detail_child_11121 (11121)
                - fake_detail_child_11122 (11122)
                - fake_detail_child_11123 (11123)

            - fake_detail_112 (112)
                - fake_detail_child_11211 (11211)
                - fake_detail_child_11212 (11212)
                - fake_detail_child_11213 (11213)

                - fake_detail_child_11221 (11221)
                - fake_detail_child_11222 (11222)
                - fake_detail_child_11223 (11223)

            - fake_detail_121 (121)
            - fake_detail_122 (122)

        - fake_parent_2 (2)
            - fake_detail_211 (211)
                - fake_detail_child_21111 (21111)
                - fake_detail_child_21112 (21112)
                - fake_detail_child_21113 (21113)
                
                - fake_detail_child_21121 (21121)
                - fake_detail_child_21122 (21122)
                - fake_detail_child_21123 (21123)

            - fake_detail_212 (212)
                - fake_detail_child_21211 (21211)
                - fake_detail_child_21212 (21212)
                - fake_detail_child_21213 (21213)
                
                - fake_detail_child_21221 (21221)
                - fake_detail_child_21222 (21222)
                - fake_detail_child_21223 (21223)

            - fake_detail_221 (221)
            - fake_detail_222 (222)

        """

        """fake_parent_1 (1)"""
        id_fake_parent_1 = ObjectId()
        fake_parent_1 = fake_parent_dao.model(
            id=id_fake_parent_1,
            code=1
        )

        """fake_detail_111 (111)"""
        id_fake_detail_111 = ObjectId()
        fake_detail_111 = fake_detail_dao_1.model(
            id=id_fake_detail_111,
            code=111,
            ipsum_model_id=id_fake_parent_1
        )

        """fake_detail_child_11111 (11111)"""
        id_fake_detail_child_11111 = ObjectId()
        fake_detail_child_11111 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_11111,
            code=11111,
            detail_parent_id=id_fake_detail_111
        )

        """fake_detail_child_11112 (11112)"""
        id_fake_detail_child_11112 = ObjectId()
        fake_detail_child_11112 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_11112,
            code=11112,
            detail_parent_id=id_fake_detail_111
        )

        """fake_detail_child_11113 (11113)"""
        id_fake_detail_child_11113 = ObjectId()
        fake_detail_child_11113 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_11113,
            code=11113,
            detail_parent_id=id_fake_detail_111
        )


        """fake_detail_child_11121 (11121)"""
        id_fake_detail_child_11121 = ObjectId()
        fake_detail_child_11121 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_11121,
            code=11121,
            detail_parent_id=id_fake_detail_111
        )

        """fake_detail_child_11122 (11122)"""
        id_fake_detail_child_11122 = ObjectId()
        fake_detail_child_11122 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_11122,
            code=11122,
            detail_parent_id=id_fake_detail_111
        )

        """fake_detail_child_11123 (11123)"""
        id_fake_detail_child_11123 = ObjectId()
        fake_detail_child_11123 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_11123,
            code=11123,
            detail_parent_id=id_fake_detail_111
        )

        """fake_detail_112 (112)"""
        id_fake_detail_112 = ObjectId()
        fake_detail_112 = fake_detail_dao_1.model(
            id=id_fake_detail_112,
            code=112,
            ipsum_model_id=id_fake_parent_1
        )

        """fake_detail_child_11211 (11211)"""
        id_fake_detail_child_11211 = ObjectId()
        fake_detail_child_11211 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_11211,
            code=11211,
            detail_parent_id=id_fake_detail_112
        )

        """fake_detail_child_11212 (11212)"""
        id_fake_detail_child_11212 = ObjectId()
        fake_detail_child_11212 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_11212,
            code=11212,
            detail_parent_id=id_fake_detail_112
        )

        """fake_detail_child_11213 (11213)"""
        id_fake_detail_child_11213 = ObjectId()
        fake_detail_child_11213 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_11213,
            code=11213,
            detail_parent_id=id_fake_detail_112
        )


        """fake_detail_child_11221 (11221)"""
        id_fake_detail_child_11221 = ObjectId()
        fake_detail_child_11221 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_11221,
            code=11221,
            detail_parent_id=id_fake_detail_112
        )

        """fake_detail_child_11222 (11222)"""
        id_fake_detail_child_11222 = ObjectId()
        fake_detail_child_11222 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_11222,
            code=11222,
            detail_parent_id=id_fake_detail_112
        )

        """fake_detail_child_11223 (11223)"""
        id_fake_detail_child_11223 = ObjectId()
        fake_detail_child_11223 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_11223,
            code=11223,
            detail_parent_id=id_fake_detail_112
        )


        """fake_detail_121 (121)"""
        id_fake_detail_121 = ObjectId()
        fake_detail_121 = fake_detail_dao_2.model(
            id=id_fake_detail_121,
            code=121,
            ipsum_model_id=id_fake_parent_1
        )

        """fake_detail_122 (122)"""
        id_fake_detail_122 = ObjectId()
        fake_detail_122 = fake_detail_dao_2.model(
            id=id_fake_detail_122,
            code=122,
            ipsum_model_id=id_fake_parent_1
        )


        """fake_parent_2 (2)"""
        id_fake_parent_2 = ObjectId()
        fake_parent_2 = fake_parent_dao.model(
            id=id_fake_parent_2,
            code=2
        )

        """fake_detail_211 (211)"""
        id_fake_detail_211 = ObjectId()
        fake_detail_211 = fake_detail_dao_1.model(
            id=id_fake_detail_211,
            code=211,
            ipsum_model_id=id_fake_parent_2
        )

        """fake_detail_child_21111 (21111)"""
        id_fake_detail_child_21111 = ObjectId()
        fake_detail_child_21111 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_21111,
            code=21111,
            detail_parent_id=id_fake_detail_211
        )

        """fake_detail_child_21112 (21112)"""
        id_fake_detail_child_21112 = ObjectId()
        fake_detail_child_21112 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_21112,
            code=21112,
            detail_parent_id=id_fake_detail_211
        )

        """fake_detail_child_21113 (21113)"""
        id_fake_detail_child_21113 = ObjectId()
        fake_detail_child_21113 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_21113,
            code=21113,
            detail_parent_id=id_fake_detail_211
        )


        """fake_detail_child_21121 (21121)"""
        id_fake_detail_child_21121 = ObjectId()
        fake_detail_child_21121 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_21121,
            code=21121,
            detail_parent_id=id_fake_detail_211
        )

        """fake_detail_child_21122 (21122)"""
        id_fake_detail_child_21122 = ObjectId()
        fake_detail_child_21122 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_21122,
            code=21122,
            detail_parent_id=id_fake_detail_211
        )

        """fake_detail_child_21123 (21123)"""
        id_fake_detail_child_21123 = ObjectId()
        fake_detail_child_21123 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_21123,
            code=21123,
            detail_parent_id=id_fake_detail_211
        )

        """fake_detail_212 (212)"""
        id_fake_detail_212 = ObjectId()
        fake_detail_212 = fake_detail_dao_1.model(
            id=id_fake_detail_212,
            code=212,
            ipsum_model_id=id_fake_parent_2
        )

        """fake_detail_child_21211 (21211)"""
        id_fake_detail_child_21211 = ObjectId()
        fake_detail_child_21211 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_21211,
            code=21211,
            detail_parent_id=id_fake_detail_212
        )

        """fake_detail_child_21212 (21212)"""
        id_fake_detail_child_21212 = ObjectId()
        fake_detail_child_21212 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_21212,
            code=21212,
            detail_parent_id=id_fake_detail_212
        )

        """fake_detail_child_21213 (21213)"""
        id_fake_detail_child_21213 = ObjectId()
        fake_detail_child_21213 = fake_detail_child_dao_1.model(
            id=id_fake_detail_child_21213,
            code=21213,
            detail_parent_id=id_fake_detail_212
        )


        """fake_detail_child_21221 (21221)"""
        id_fake_detail_child_21221 = ObjectId()
        fake_detail_child_21221 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_21221,
            code=21221,
            detail_parent_id=id_fake_detail_212
        )

        """fake_detail_child_21222 (21222)"""
        id_fake_detail_child_21222 = ObjectId()
        fake_detail_child_21222 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_21222,
            code=21222,
            detail_parent_id=id_fake_detail_212
        )

        """fake_detail_child_21223 (21223)"""
        id_fake_detail_child_21223 = ObjectId()
        fake_detail_child_21223 = fake_detail_child_dao_2.model(
            id=id_fake_detail_child_21223,
            code=21223,
            detail_parent_id=id_fake_detail_212
        )

        """fake_detail_221 (221)"""
        id_fake_detail_221 = ObjectId()
        fake_detail_221 = fake_detail_dao_2.model(
            id=id_fake_detail_221,
            code=221,
            ipsum_model_id=id_fake_parent_2
        )

        """fake_detail_222 (222)"""
        id_fake_detail_222 = ObjectId()
        fake_detail_222 = fake_detail_dao_2.model(
            id=id_fake_detail_222,
            code=222,
            ipsum_model_id=id_fake_parent_2
        )

        database_test = DatabaseTest(host=get_test_database_url())

        database_test.add_data(fake_parent_dao, fake_parent_1)
        database_test.add_data(fake_detail_dao_1, [fake_detail_111, fake_detail_112], [id_fake_parent_1])
        database_test.add_data(fake_detail_child_dao_1, [fake_detail_child_11111, fake_detail_child_11112, fake_detail_child_11113], [id_fake_detail_111])
        database_test.add_data(fake_detail_child_dao_2, [fake_detail_child_11121, fake_detail_child_11122, fake_detail_child_11123], [id_fake_detail_111])
        
        database_test.add_data(fake_detail_child_dao_1, [fake_detail_child_11211, fake_detail_child_11212, fake_detail_child_11213], id_fake_detail_112)
        database_test.add_data(fake_detail_child_dao_2, [fake_detail_child_11221, fake_detail_child_11222, fake_detail_child_11223], id_fake_detail_112)

        database_test.add_data(fake_detail_dao_2, [fake_detail_121, fake_detail_122], [id_fake_parent_1])



        database_test.add_data(fake_parent_dao, fake_parent_2)
        database_test.add_data(fake_detail_dao_1, [fake_detail_211, fake_detail_212], [id_fake_parent_2])
        database_test.add_data(fake_detail_child_dao_1, [fake_detail_child_21111, fake_detail_child_21112, fake_detail_child_21113], [id_fake_detail_211])
        database_test.add_data(fake_detail_child_dao_2, [fake_detail_child_21121, fake_detail_child_21122, fake_detail_child_21123], [id_fake_detail_211])
    
        database_test.add_data(fake_detail_child_dao_1, [fake_detail_child_21211, fake_detail_child_21212, fake_detail_child_21213], [id_fake_detail_212])
        database_test.add_data(fake_detail_child_dao_2, [fake_detail_child_21221, fake_detail_child_21222, fake_detail_child_21223], [id_fake_detail_212])
        
        database_test.add_data(fake_detail_dao_2, [fake_detail_221, fake_detail_222], [id_fake_parent_2])


        """ Test """
        
        @database_test.persistence_test()
        def _test_delete_fake_parent_1():

            fake_parent_dao.cascade.delete(fake_parent_1.id)

            assert not fake_parent_dao.find_by_id(fake_parent_1.id) is None

            assert fake_detail_dao_1.find_by_id(fake_detail_111.id) is None
            assert fake_detail_dao_1.find_by_id(fake_detail_112.id) is None

            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11111.id) is None
            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11112.id) is None
            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11113.id) is None

            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11121.id) is None
            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11122.id) is None
            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11123.id) is None

            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11211.id) is None
            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11212.id) is None
            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11213.id) is None

            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11221.id) is None
            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11222.id) is None
            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11223.id) is None

            assert fake_detail_dao_2.find_by_id(fake_detail_121.id) is None
            assert fake_detail_dao_2.find_by_id(fake_detail_122.id) is None



            assert not fake_parent_dao.find_by_id(fake_parent_2.id) is None

            assert not fake_detail_dao_1.find_by_id(fake_detail_211.id) is None
            assert not fake_detail_dao_1.find_by_id(fake_detail_212.id) is None

            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21111.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21112.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21113.id) is None

            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21221.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21222.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21223.id) is None


            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21211.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21212.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21213.id) is None

            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21221.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21222.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21223.id) is None

            assert not fake_detail_dao_2.find_by_id(fake_detail_221.id) is None
            assert not fake_detail_dao_2.find_by_id(fake_detail_222.id) is None

        _test_delete_fake_parent_1()
        

        @database_test.persistence_test()
        def _test_delete_fake_detail_112():

            fake_detail_dao_1.cascade.delete(fake_detail_112.id)

            assert not fake_parent_dao.find_by_id(fake_parent_1.id) is None

            assert not fake_detail_dao_1.find_by_id(fake_detail_111.id) is None
            assert not fake_detail_dao_1.find_by_id(fake_detail_112.id) is None

            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_11111.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_11112.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_11113.id) is None

            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_11121.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_11122.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_11123.id) is None

            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11211.id) is None
            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11212.id) is None
            assert fake_detail_child_dao_1.find_by_id(fake_detail_child_11213.id) is None

            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11221.id) is None
            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11222.id) is None
            assert fake_detail_child_dao_2.find_by_id(fake_detail_child_11223.id) is None

            assert not fake_detail_dao_2.find_by_id(fake_detail_121.id) is None
            assert not fake_detail_dao_2.find_by_id(fake_detail_122.id) is None



            assert not fake_parent_dao.find_by_id(fake_parent_2.id) is None

            assert not fake_detail_dao_1.find_by_id(fake_detail_211.id) is None
            assert not fake_detail_dao_1.find_by_id(fake_detail_212.id) is None

            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21111.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21112.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21113.id) is None

            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21221.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21222.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21223.id) is None


            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21211.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21212.id) is None
            assert not fake_detail_child_dao_1.find_by_id(fake_detail_child_21213.id) is None

            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21221.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21222.id) is None
            assert not fake_detail_child_dao_2.find_by_id(fake_detail_child_21223.id) is None

            assert not fake_detail_dao_2.find_by_id(fake_detail_221.id) is None
            assert not fake_detail_dao_2.find_by_id(fake_detail_222.id) is None

        _test_delete_fake_detail_112()
