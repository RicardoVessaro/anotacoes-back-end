
from pytest import raises
from arq.data.dao.dao import Dao
from arq.exception.arq_exception import ArqException
from arq.exception.exception_message import PAGE_NOT_FOUND_EXCEPTION_MESSAGE
from arq.service.service import Service
from arq.tests.resources.data.model.arq_test_model import ArqTestModel
from arq.util.enviroment_variable import get_test_database_url
from arq.util.test.database_test import DatabaseTest

class TestArqService:

    TEST_DB_URI = get_test_database_url()

    arq_service = Service(dao=Dao(model=ArqTestModel))

    dao = arq_service._dao

    model = dao.model

    def test_insert(self):
        arq_test_model = ArqTestModel(code=1, title='test_insert_TestArqDao')

        arq_database_test = DatabaseTest(host=self.TEST_DB_URI, daos_to_clean=[self.dao])
        @arq_database_test.persistence_test()
        def _():
            
            inserted_model = self.arq_service.insert(arq_test_model)
            db_model = self.model.objects().first()

            assert inserted_model.id == db_model.id

        _()

    def test_delete(self):
        arq_test_model, arq_database_test = self._build_default_model_and_arq_test(1, 'test_delete_TestArqDao')
        
        @arq_database_test.persistence_test()
        def _():
            arq_test_model_id = str(arq_test_model.id)

            deleted_id = self.arq_service.delete(arq_test_model_id)

            assert deleted_id == arq_test_model_id

            assert self.arq_service.find_by_id(arq_test_model_id) is None

        _()

    def test_find_by_id(self):
        arq_test_model, arq_database_test = self._build_default_model_and_arq_test(1, 'test_find_by_idTestArqDao')
        @arq_database_test.persistence_test()
        def _():

            def test_find_by_id_using_string():
                arq_test_model_id_str = str(arq_test_model.id)

                bd_model = self.arq_service.find_by_id(arq_test_model_id_str)

                assert bd_model.id == arq_test_model.id
                assert bd_model.code == arq_test_model.code
                assert bd_model.title == arq_test_model.title

            test_find_by_id_using_string()

            def test_find_by_id_using_object_id():
                arq_test_model_id = arq_test_model.id

                bd_model = self.arq_service.find_by_id(arq_test_model_id)

                assert bd_model.id == arq_test_model.id
                assert bd_model.code == arq_test_model.code
                assert bd_model.title == arq_test_model.title

            test_find_by_id_using_object_id()

        _()

    def test_find(self):
        arq_test_model_1 = ArqTestModel(code=1, title='test_find_TestArqDao_1', boolean=True, tags=['A', 'B', 'C'])
        arq_test_model_2 = ArqTestModel(code=2, title='test_find_TestArqDao_2', boolean=False, tags=['A', 'B', 'D'])
        arq_test_model_3 = ArqTestModel(code=3, title='test_find_TestArqDao_3', boolean=True, tags=['B', 'C', 'D'])

        arq_database_test = DatabaseTest(host=self.TEST_DB_URI)
        arq_database_test.add_data(self.dao, arq_test_model_1)
        arq_database_test.add_data(self.dao, arq_test_model_2)
        arq_database_test.add_data(self.dao, arq_test_model_3)
        @arq_database_test.persistence_test()
        def _():

            expected_ids = [arq_test_model_1.id, arq_test_model_2.id, arq_test_model_3.id]
            results = self.arq_service.find()
            for result in results:
                assert result.id in expected_ids

            results = self.arq_service.find(code=2)
            for result in results:
                assert result.id == arq_test_model_2.id

            results = self.arq_service.find(title='test_find_TestArqDao_3')
            for result in results:
                assert result.id == arq_test_model_3.id

            expected_ids = [arq_test_model_1.id, arq_test_model_3.id]
            results = self.arq_service.find(boolean=True)
            for result in results:
                assert result.id in expected_ids

            results = self.arq_service.find(boolean=True, code=3)
            for resultd in results:
                assert resultd.id == arq_test_model_3.id

            expected_ids = [arq_test_model_1.id, arq_test_model_2.id]
            results = self.arq_service.find(code=[1, 2])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [arq_test_model_1.id, arq_test_model_3.id]
            results = self.arq_service.find(title=['test_find_TestArqDao_1', 'test_find_TestArqDao_3'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [arq_test_model_2.id, arq_test_model_3.id]
            results = self.arq_service.find(tags='D')
            for result in results:
                assert result.id in expected_ids

            expected_ids = [arq_test_model_2.id, arq_test_model_3.id]
            results = self.arq_service.find(tags=['D'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [arq_test_model_1.id, arq_test_model_2.id]
            results = self.arq_service.find(tags=['A'])
            for result in results:
                assert result.id in expected_ids

            expected_ids = [arq_test_model_1.id, arq_test_model_2.id, arq_test_model_3.id]
            results = self.arq_service.find(tags=['A', 'B'])
            for result in results:
                assert result.id in expected_ids

        _()

    def test_paginate(self):
        arq_test_model_list = self._build_arq_test_model_list()

        arq_database_test = DatabaseTest(host=self.TEST_DB_URI)
        arq_database_test.add_data(self.dao, arq_test_model_list)
        @arq_database_test.persistence_test()
        def _():
            model_ids, boolean_model_ids = self._get_model_ids(arq_test_model_list)

            def test_default_pagination():
                pagination = self.arq_service.paginate()

                assert pagination['page'] == 1
                assert pagination['limit'] == 5
                assert pagination['total'] == 15
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[0:5]

            test_default_pagination()


            def test_paginate_with_filter():
                pagination = self.arq_service.paginate(boolean=False)

                assert pagination['page'] == 1
                assert pagination['limit'] == 5
                assert pagination['total'] == 15 - len(boolean_model_ids)
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == True

                for item in pagination['items']:
                    assert item.id not in boolean_model_ids
            
            test_paginate_with_filter()


            def test_paginate_limit_7_in_results():
                pagination = self.arq_service.paginate(limit=7)

                assert pagination['page'] == 1
                assert pagination['limit'] == 7
                assert pagination['total'] == 15
                assert pagination['has_prev'] == False
                assert pagination['has_next'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[0:7]

            test_paginate_limit_7_in_results()

            
            def test_paginate_with_filter_and_limit_3_in_results():
                pagination = self.arq_service.paginate(boolean=True, limit=3, page=2)

                assert pagination['page'] == 2
                assert pagination['limit'] == 3
                assert pagination['total'] == len(boolean_model_ids)
                assert pagination['has_prev'] == True
                assert pagination['has_next'] == True

                for item in pagination['items']:
                    assert item.id in boolean_model_ids
                    assert item.id in boolean_model_ids[3:6]
            
            test_paginate_with_filter_and_limit_3_in_results()


            def test_paginate_limit_7_page_2_in_results():
                pagination = self.arq_service.paginate(limit=7, page=2)

                assert pagination['page'] == 2
                assert pagination['limit'] == 7
                assert pagination['total'] == 15
                assert pagination['has_prev'] == True
                assert pagination['has_next'] == True

                for item in pagination['items']:
                    assert item.id in model_ids[7:14]

            test_paginate_limit_7_page_2_in_results()

            def test_paginate_limit_7_page_3_in_results():
                pagination = self.arq_service.paginate(limit=7, page=3)

                assert pagination['page'] == 3
                assert pagination['limit'] == 7
                assert pagination['total'] == 15
                assert pagination['has_prev'] == True
                assert pagination['has_next'] == False

                for item in pagination['items']:
                    assert item.id in model_ids[14:15]

            test_paginate_limit_7_page_3_in_results()


            def test_paginate_must_raise_exception_when_page_is_greater_than_pages():

                with raises(ArqException, match=PAGE_NOT_FOUND_EXCEPTION_MESSAGE.format(4, 3)):
                    pagination = self.arq_service.paginate(page=4, limit=5)

            test_paginate_must_raise_exception_when_page_is_greater_than_pages()

        _()

    def _build_arq_test_model_list(self):
        arq_test_model_list = []
        
        boolean = True
        for i in range(15):
            arq_test_model = ArqTestModel(
                code=i, 
                title='test_find_TestArqDao_'+str(i), 
                boolean=boolean
            )

            boolean = not boolean

            arq_test_model_list.append(arq_test_model)

        return arq_test_model_list

    def _get_model_ids(self, models):
        ids = []
        boolean_ids = []
        
        for model in models:
            model_id = model.id
            ids.append(model_id)

            if model.boolean:
                boolean_ids.append(model_id)

        return ids, boolean_ids

    def _build_default_model_and_arq_test(self, code, title):
        arq_test_model = ArqTestModel(code=code, title=title)

        arq_database_test = DatabaseTest(host=self.TEST_DB_URI)
        arq_database_test.add_data(self.dao, arq_test_model)
        
        return arq_test_model, arq_database_test