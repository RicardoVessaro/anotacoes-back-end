
from operator import le
from arq.util.test.database_test import DatabaseTest
from arq.data.dao.dao import Dao
from arq.tests.resources.data.model.arq_test_model import ArqTestModel

class TestArqDatabaseTest:

    TEST_DB_URI = "mongodb+srv://user:senha@anotacoes-cluster.jwtdf.mongodb.net/anotacoes-test?retryWrites=true&w=majority"

    arq_dao = Dao(model=ArqTestModel)

    def test_add_data(self):

        def test_using_one_item():
            arq_database_test = DatabaseTest()

            model = ArqTestModel(code=1, title="test_using_one_item")
            arq_database_test.add_data(self.arq_dao, model)
            
            assert len(arq_database_test.data_to_insert) == 1
            data_to_insert_0 = arq_database_test.data_to_insert[0]
            assert data_to_insert_0[0] == self.arq_dao
            assert data_to_insert_0[1] == model

            other_model = ArqTestModel(code=2, title="test_using_one_item 2")
            arq_database_test.add_data(self.arq_dao, other_model)
            
            assert len(arq_database_test.data_to_insert) == 2

            data_to_insert_0 = arq_database_test.data_to_insert[0]
            assert data_to_insert_0[0] == self.arq_dao
            assert data_to_insert_0[1] == model

            data_to_insert_1 = arq_database_test.data_to_insert[1]
            assert data_to_insert_1[0] == self.arq_dao
            assert data_to_insert_1[1] == other_model

        test_using_one_item()

        def test_using_list():

            model_0 = ArqTestModel(code=0, title="test_using_one_item")
            model_1 = ArqTestModel(code=1, title="test_using_one_item")

            arq_database_test = DatabaseTest()
            arq_database_test.add_data(self.arq_dao, [model_0, model_1])
            assert len(arq_database_test.data_to_insert) == 2

            data_to_insert_0 = arq_database_test.data_to_insert[0]
            assert data_to_insert_0[0] == self.arq_dao
            assert data_to_insert_0[1] == model_0

            data_to_insert_1 = arq_database_test.data_to_insert[1]
            assert data_to_insert_1[0] == self.arq_dao
            assert data_to_insert_1[1] == model_1


            model_2 = ArqTestModel(code=2, title="test_using_one_item")
            model_3 = ArqTestModel(code=3, title="test_using_one_item")

            arq_database_test.add_data(self.arq_dao, [model_2, model_3])
            assert len(arq_database_test.data_to_insert) == 4

            data_to_insert_2 = arq_database_test.data_to_insert[2]
            assert data_to_insert_2[0] == self.arq_dao
            assert data_to_insert_2[1] == model_2

            data_to_insert_3 = arq_database_test.data_to_insert[3]
            assert data_to_insert_3[0] == self.arq_dao
            assert data_to_insert_3[1] == model_3

        test_using_list()

    def test_insert_data(self):

        def test_method():
            model = ArqTestModel(code=1, title="test_using_one_item")

            arq_database_test = DatabaseTest()
            arq_database_test.add_data(self.arq_dao, model)

            arq_database_test._connect(host=self.TEST_DB_URI)
            arq_database_test._clean_existing_data()

            arq_database_test._insert_data()

            database_model = self.arq_dao.find().first()
            
            assert not database_model is None
            assert database_model.id == model.id

            arq_database_test._delete_data()
            arq_database_test._disconnect()


        test_method()

        def test_in_decorator():

            model = ArqTestModel(code=1, title="test_using_one_item")

            arq_database_test = DatabaseTest()
            arq_database_test.add_data(self.arq_dao, model)
            
            @arq_database_test.persistence_test(host=self.TEST_DB_URI)
            def _():
                database_model = self.arq_dao.find().first()
                
                assert not database_model is None
                assert database_model.id == model.id

            _()

        test_in_decorator()

    def test_clean_existing_data(self):

        def test_method():

            def _test_cleaning_data_to_insert():
                model = ArqTestModel(code=1, title="test_using_one_item")

                arq_database_test = DatabaseTest()
                arq_database_test.add_data(self.arq_dao, model)

                arq_database_test._connect(host=self.TEST_DB_URI)
                arq_database_test._clean_existing_data()

                arq_database_test._insert_data()

                arq_database_test._clean_existing_data()

                database_model = self.arq_dao.find().first()
                
                assert database_model is None

                arq_database_test._delete_data()
                arq_database_test._disconnect()

            _test_cleaning_data_to_insert()

            def _test_cleaning_daos_to_clean():

                model = ArqTestModel(code=1, title="test_using_one_item")

                arq_database_test = DatabaseTest(daos_to_clean=[self.arq_dao])
                arq_database_test._connect(host=self.TEST_DB_URI)
                arq_database_test._clean_existing_data()

                self.arq_dao.insert(model)

                arq_database_test._clean_existing_data()

                database_model = self.arq_dao.find().first()
                
                assert database_model is None

                arq_database_test._delete_data()
                arq_database_test._disconnect()

            _test_cleaning_daos_to_clean()


        test_method()

        def test_decorator():

            def _test_cleaning_data_to_insert():

                model = ArqTestModel(code=1, title="test_using_one_item")

                arq_database_test = DatabaseTest()
                arq_database_test.add_data(self.arq_dao, model)
                
                @arq_database_test.persistence_test(host=self.TEST_DB_URI)
                def _():
                    arq_database_test._clean_existing_data()

                    database_model = self.arq_dao.find().first()

                    assert database_model is None

                _()

            _test_cleaning_data_to_insert()

            def _test_cleaning_daos_to_clean():
                model = ArqTestModel(code=1, title="test_using_one_item")

                arq_database_test = DatabaseTest(daos_to_clean=[self.arq_dao])
                @arq_database_test.persistence_test(host=self.TEST_DB_URI)
                def _():
                    self.arq_dao.insert(model)

                    arq_database_test._clean_existing_data()

                    database_model = self.arq_dao.find().first()
                    
                    assert database_model is None
                _()

            _test_cleaning_daos_to_clean()

        test_decorator()

    def test_delete_data(self):

        def test_method():

            model = ArqTestModel(code=1, title="test_using_one_item")

            arq_database_test = DatabaseTest()
            arq_database_test.add_data(self.arq_dao, model)

            arq_database_test._connect(host=self.TEST_DB_URI)
            arq_database_test._clean_existing_data()

            arq_database_test._insert_data()

            arq_database_test._delete_data()

            database_model = self.arq_dao.find().first()
            
            assert database_model is None

            arq_database_test._delete_data()
            arq_database_test._disconnect()

        test_method()

        def test_decorator():

            model = ArqTestModel(code=1, title="test_using_one_item")

            arq_database_test = DatabaseTest()
            arq_database_test.add_data(self.arq_dao, model)
            
            @arq_database_test.persistence_test(host=self.TEST_DB_URI)
            def _():
                arq_database_test._delete_data()

                database_model = self.arq_dao.find().first()

                assert database_model is None

            _()

        test_decorator()
    