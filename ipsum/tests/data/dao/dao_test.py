

import datetime
from pytest import raises
from ipsum.data.cascade import Cascade
from ipsum.data.dao.dao import DAO
from ipsum.data.dao.detail_crud_dao import DetailCRUDDAO
from ipsum.exception.exception_message import PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.util.enviroment_variable import get_test_database_url
from ipsum.util.object_util import is_none_or_empty
from ipsum.util.test.database_test import DatabaseTest
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.tests.resources.data.model.detail_test_model import DetailTestModel
from ipsum.tests.resources.data.model.detail_child_test_model import DetailChildTestModel

class TestDao:

    TEST_DB_URI = get_test_database_url()

    dao = DAO(model=IpsumTestModel)

    model = dao.model

    def test_insert(self):
        ipsum_test_model = IpsumTestModel(code=1, title='test_insert_TestDao')

        ipsum_database_test = DatabaseTest(host=self.TEST_DB_URI, daos_to_clean=[self.dao])
        @ipsum_database_test.persistence_test()
        def _():
            
            inserted_model = self.dao.insert(ipsum_test_model)
            db_model = self.model.objects().first()

            assert inserted_model.id == db_model.id

        _()

    def test_delete_using_str(self):
        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_using_str')
        
        @ipsum_database_test.persistence_test()
        def _():
            ipsum_test_model_id = str(ipsum_test_model.id)

            deleted_id = self.dao.delete(ipsum_test_model_id)

            assert deleted_id == ipsum_test_model_id

            assert self.dao.find_by_id(ipsum_test_model_id) is None

        _()

    def test_has_cascade(self):
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

        class EmptyChildDAO(DAO):
            def __init__(self) -> None:
                super().__init__(
                    model=IpsumTestModel, 
                    cascade=Cascade(childs=[])
                )

        assert True == FakeParentDAO().has_cascade()
        assert True == FakeDetailDAO().has_cascade()
        assert False == FakeDetailChildDAO().has_cascade()
        assert False == EmptyChildDAO().has_cascade()


    def test_delete_using_object_id(self):
        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_using_object_id')
        
        @ipsum_database_test.persistence_test()
        def _():
            ipsum_test_model_id = ipsum_test_model.id

            deleted_id = self.dao.delete(ipsum_test_model_id)

            assert deleted_id == str(ipsum_test_model_id)

            assert self.dao.find_by_id(ipsum_test_model_id) is None

        _()

    def test_delete_using_model(self):
        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_using_model')
        
        @ipsum_database_test.persistence_test()
        def _():
            ipsum_test_model_id = str(ipsum_test_model.id)

            deleted_id = self.dao.delete(ipsum_test_model)

            assert deleted_id == str(ipsum_test_model_id)

            assert self.dao.find_by_id(ipsum_test_model_id) is None

        _()

    def test_delete_using_iterable(self):
        ipsum_test_model_1 = IpsumTestModel(code=1, title="model 1")
        ipsum_test_model_2 = IpsumTestModel(code=2, title="model 2")

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.dao, [ipsum_test_model_1, ipsum_test_model_2])

        @database_test.persistence_test()
        def _():
            models = self.dao.find()
            
            deleted_ids = self.dao.delete(models)

            assert str(ipsum_test_model_1.id) in deleted_ids
            assert str(ipsum_test_model_2.id) in deleted_ids

            assert self.dao.find_by_id(ipsum_test_model_1.id) is None
            assert self.dao.find_by_id(ipsum_test_model_2.id) is None

        _()

    def test_find_by_id(self):
        ipsum_test_model, ipsum_database_test = self._build_default_model_and_ipsum_test(1, 'test_find_by_idTestDao')
        @ipsum_database_test.persistence_test()
        def _():

            def test_find_by_id_using_string():
                ipsum_test_model_id_str = str(ipsum_test_model.id)

                bd_model = self.dao.find_by_id(ipsum_test_model_id_str)

                assert bd_model.id == ipsum_test_model.id
                assert bd_model.code == ipsum_test_model.code
                assert bd_model.title == ipsum_test_model.title

            test_find_by_id_using_string()

            def test_find_by_id_using_object_id():
                ipsum_test_model_id = ipsum_test_model.id

                bd_model = self.dao.find_by_id(ipsum_test_model_id)

                assert bd_model.id == ipsum_test_model.id
                assert bd_model.code == ipsum_test_model.code
                assert bd_model.title == ipsum_test_model.title

            test_find_by_id_using_object_id()

        _()

    def test_find(self):
        today = datetime.date.today()

        ipsum_test_model_1 = IpsumTestModel(code=1, title='test_find_TestDao_1', boolean=True, tags=['A', 'B', 'C'])
        ipsum_test_model_2 = IpsumTestModel(code=2, title='test_find_TestDao_2', boolean=False, tags=['A', 'B', 'D'], day=today)
        ipsum_test_model_3 = IpsumTestModel(code=3, title='test_find_TestDao_3', boolean=True, tags=['B', 'C', 'D'], day=today)

        ipsum_database_test = DatabaseTest(host=self.TEST_DB_URI)
        ipsum_database_test.add_data(self.dao, ipsum_test_model_1)
        ipsum_database_test.add_data(self.dao, ipsum_test_model_2)
        ipsum_database_test.add_data(self.dao, ipsum_test_model_3)
        @ipsum_database_test.persistence_test()
        def _():

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.dao.find()
            for result in results:
                assert result.id in expected_ids

            results = self.dao.find(code=2)
            for result in results:
                assert result.id == ipsum_test_model_2.id

            results = self.dao.find(title='test_find_TestDao_3')
            for result in results:
                assert result.id == ipsum_test_model_3.id

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_3.id]
            results = self.dao.find(boolean=True)
            for result in results:
                assert result.id in expected_ids

            results = self.dao.find(boolean=True, code=3)
            for resultd in results:
                assert resultd.id == ipsum_test_model_3.id

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id]
            results = self.dao.find(code=[1, 2])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_3.id]
            results = self.dao.find(title=['test_find_TestDao_1', 'test_find_TestDao_3'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.dao.find(tags='D')
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.dao.find(tags=['D'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id]
            results = self.dao.find(tags=['A'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.dao.find(tags=['A', 'B'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.dao.find(day=today)
            for result in results:
                assert result.id in expected_ids

        _()

    def test_paginate(self):
        ipsum_test_model_list = self._build_ipsum_test_model_list()

        ipsum_database_test = DatabaseTest(host=self.TEST_DB_URI)
        ipsum_database_test.add_data(self.dao, ipsum_test_model_list)
        @ipsum_database_test.persistence_test()
        def _():
            model_ids, boolean_model_ids = self._get_model_ids(ipsum_test_model_list)

            def test_default_pagination():
                pagination = self.dao.paginate()

                assert pagination['page'] == 1
                assert pagination['limit'] == 5
                assert pagination['total'] == 15
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == True
                assert pagination['has_result'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[0:5]

            test_default_pagination()


            def test_paginate_with_filter():
                pagination = self.dao.paginate(boolean=False)

                assert pagination['page'] == 1
                assert pagination['limit'] == 5
                assert pagination['total'] == 15 - len(boolean_model_ids)
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == True
                assert pagination['has_result'] == True

                for item in pagination['items']:
                    assert item.id not in boolean_model_ids
            
            test_paginate_with_filter()


            def test_paginate_limit_7_in_results():
                pagination = self.dao.paginate(limit=7)

                assert pagination['page'] == 1
                assert pagination['limit'] == 7
                assert pagination['total'] == 15
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == True
                assert pagination['has_result'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[0:7]

            test_paginate_limit_7_in_results()

            def test_paginate_with_filter_and_limit_3_in_results():
                pagination = self.dao.paginate(boolean=True, limit=3, page=2)

                assert pagination['page'] == 2
                assert pagination['limit'] == 3
                assert pagination['total'] == len(boolean_model_ids)
                assert pagination['has_prev'] == True
                assert pagination['has_next'] == True
                assert pagination['has_result'] == True

                for item in pagination['items']:
                    assert item.id in boolean_model_ids
                    assert item.id in boolean_model_ids[3:6]
            
            test_paginate_with_filter_and_limit_3_in_results()


            def test_paginate_limit_7_page_2_in_results():
                pagination = self.dao.paginate(limit=7, page=2)

                assert pagination['page'] == 2
                assert pagination['limit'] == 7
                assert pagination['total'] == 15
                assert pagination['has_prev'] == True
                assert pagination['has_next'] == True
                assert pagination['has_result'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[7:14]

            test_paginate_limit_7_page_2_in_results()

            def test_paginate_limit_7_page_3_in_results():
                pagination = self.dao.paginate(limit=7, page=3)

                assert pagination['page'] == 3
                assert pagination['limit'] == 7
                assert pagination['total'] == 15
                assert pagination['has_prev'] == True
                assert pagination['has_next'] == False
                assert pagination['has_result'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[14:15]

            test_paginate_limit_7_page_3_in_results()


            def test_paginate_must_raise_exception_when_page_is_greater_than_pages():

                with raises(IpsumException, match=PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(4, 3)):
                    pagination = self.dao.paginate(page=4, limit=5)

            test_paginate_must_raise_exception_when_page_is_greater_than_pages()

            def test_must_return_empty_when_not_found_in_filter():
                pagination = self.dao.paginate(title='Nothing')

                assert pagination['page'] == 0
                assert pagination['limit'] == 0
                assert pagination['total'] == 0
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == False
                assert pagination['has_result'] == False
                assert is_none_or_empty(pagination['items'])

            test_must_return_empty_when_not_found_in_filter()

        _()

    def _build_ipsum_test_model_list(self):
        ipsum_test_model_list = []
        
        boolean = True
        for i in range(15):
            ipsum_test_model = IpsumTestModel(
                code=i, 
                title='test_find_TestDao_'+str(i), 
                boolean=boolean
            )

            boolean = not boolean

            ipsum_test_model_list.append(ipsum_test_model)

        return ipsum_test_model_list

    def _get_model_ids(self, models):
        ids = []
        boolean_ids = []
        
        for model in models:
            model_id = model.id
            ids.append(model_id)

            if model.boolean:
                boolean_ids.append(model_id)

        return ids, boolean_ids


    def _build_default_model_and_ipsum_test(self, code, title):
        ipsum_test_model = IpsumTestModel(code=code, title=title)

        ipsum_database_test = DatabaseTest(host=self.TEST_DB_URI)
        ipsum_database_test.add_data(self.dao, ipsum_test_model)
        
        return ipsum_test_model, ipsum_database_test

    

