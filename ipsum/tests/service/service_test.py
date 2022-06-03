
import datetime
from pytest import raises
from ipsum.data.dao.dao import DAO
from ipsum.exception.ipsum_exception import IpsumException
from ipsum.exception.exception_message import PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from ipsum.service.service import Service
from ipsum.tests.resources.data.model.ipsum_test_model import IpsumTestModel
from ipsum.util.enviroment_variable import get_test_database_url
from ipsum.util.object_util import is_none_or_empty
from ipsum.util.test.database_test import DatabaseTest

class TestService:

    TEST_DB_URI = get_test_database_url()

    service = Service(dao=DAO(model=IpsumTestModel))

    dao = service._dao

    model = dao.model

    def test_insert(self):
        ipsum_test_model = IpsumTestModel(code=1, title='test_insert_TestService')

        database_test = DatabaseTest(host=self.TEST_DB_URI, daos_to_clean=[self.dao])
        @database_test.persistence_test()
        def _():
            
            inserted_model = self.service.insert(ipsum_test_model)
            db_model = self.model.objects().first()

            assert inserted_model.id == db_model.id

        _()

    def test_delete(self):
        ipsum_test_model, database_test = self._build_default_model_and_ipsum_test(1, 'test_delete_TestService')
        
        @database_test.persistence_test()
        def _():
            ipsum_test_model_id = str(ipsum_test_model.id)

            deleted_id = self.service.delete(ipsum_test_model_id)

            assert deleted_id == ipsum_test_model_id

            assert self.service.find_by_id(ipsum_test_model_id) is None

        _()

    def test_find_by_id(self):
        ipsum_test_model, database_test = self._build_default_model_and_ipsum_test(1, 'test_find_by_idTestService')
        @database_test.persistence_test()
        def _():

            def test_find_by_id_using_string():
                ipsum_test_model_id_str = str(ipsum_test_model.id)

                bd_model = self.service.find_by_id(ipsum_test_model_id_str)

                assert bd_model.id == ipsum_test_model.id
                assert bd_model.code == ipsum_test_model.code
                assert bd_model.title == ipsum_test_model.title

            test_find_by_id_using_string()

            def test_find_by_id_using_object_id():
                ipsum_test_model_id = ipsum_test_model.id

                bd_model = self.service.find_by_id(ipsum_test_model_id)

                assert bd_model.id == ipsum_test_model.id
                assert bd_model.code == ipsum_test_model.code
                assert bd_model.title == ipsum_test_model.title

            test_find_by_id_using_object_id()

        _()

    def test_find(self):
        today = datetime.date.today()

        ipsum_test_model_1 = IpsumTestModel(code=1, title='test_find_TestService_1', boolean=True, tags=['A', 'B', 'C'])
        ipsum_test_model_2 = IpsumTestModel(code=2, title='test_find_TestService_2', boolean=False, tags=['A', 'B', 'D'], day=today)
        ipsum_test_model_3 = IpsumTestModel(code=3, title='test_find_TestService_3', boolean=True, tags=['B', 'C', 'D'], day=today)

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.dao, ipsum_test_model_1)
        database_test.add_data(self.dao, ipsum_test_model_2)
        database_test.add_data(self.dao, ipsum_test_model_3)
        @database_test.persistence_test()
        def _():

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.service.find()
            for result in results:
                assert result.id in expected_ids

            results = self.service.find(code=2)
            for result in results:
                assert result.id == ipsum_test_model_2.id

            results = self.service.find(title='test_find_TestService_3')
            for result in results:
                assert result.id == ipsum_test_model_3.id

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_3.id]
            results = self.service.find(boolean=True)
            for result in results:
                assert result.id in expected_ids

            results = self.service.find(boolean=True, code=3)
            for resultd in results:
                assert resultd.id == ipsum_test_model_3.id

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id]
            results = self.service.find(code=[1, 2])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_3.id]
            results = self.service.find(title=['test_find_TestService_1', 'test_find_TestService_3'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.service.find(tags='D')
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.service.find(tags=['D'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id]
            results = self.service.find(tags=['A'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_1.id, ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.service.find(tags=['A', 'B'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [ipsum_test_model_2.id, ipsum_test_model_3.id]
            results = self.service.find(day=today)
            for result in results:
                assert result.id in expected_ids

        _()

    def test_paginate(self):
        ipsum_test_model_list = self._build_ipsum_test_model_list()

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.dao, ipsum_test_model_list)
        @database_test.persistence_test()
        def _():
            model_ids, boolean_model_ids = self._get_model_ids(ipsum_test_model_list)

            def test_default_pagination():
                pagination = self.service.paginate()

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
                pagination = self.service.paginate(boolean=False)

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
                pagination = self.service.paginate(limit=7)

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
                pagination = self.service.paginate(boolean=True, limit=3, page=2)

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
                pagination = self.service.paginate(limit=7, page=2)

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
                pagination = self.service.paginate(limit=7, page=3)

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
                    pagination = self.service.paginate(page=4, limit=5)

            test_paginate_must_raise_exception_when_page_is_greater_than_pages()

            def test_must_return_empty_when_not_found_in_filter():
                pagination = self.service.paginate(title='Nothing')

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
                title='test_find_TestService_'+str(i), 
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

        database_test = DatabaseTest(host=self.TEST_DB_URI)
        database_test.add_data(self.dao, ipsum_test_model)
        
        return ipsum_test_model, database_test