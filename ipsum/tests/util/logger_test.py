
from datetime import datetime
from unittest.mock import patch
from ipsum.util.logger import Logger


class TestLogger:

    class TestClass:
            pass

    def test_class_name(self):

        assert str(self.TestClass().__class__) == Logger(self.TestClass()).class_name()

    def test_levels(self):
        
        logger = Logger(self.TestClass())

        with patch('ipsum.util.logger.get_enviroment_variable') as mock_get_enviroment_variable:
            
            mock_get_enviroment_variable.return_value = logger.INFO
            assert logger.levels() == [logger.INFO]

            mock_get_enviroment_variable.return_value = logger.WARNING
            assert logger.levels() == [logger.INFO, logger.WARNING]

            mock_get_enviroment_variable.return_value = logger.ERROR
            assert logger.levels() == [logger.INFO, logger.WARNING, logger.ERROR]

    def test_logging_levels(self):

        logger = Logger(self.TestClass())

        def _must_return_none_when_level_is_info_and_log_is_warning_or_error():

            with patch('ipsum.util.logger.get_enviroment_variable') as mock_get_enviroment_variable:
            
                mock_get_enviroment_variable.return_value = logger.INFO

                assert logger.warnning('warning') is None
                assert logger.error('error') is None

        _must_return_none_when_level_is_info_and_log_is_warning_or_error()

        def _must_return_none_when_level_is_warning_and_log_is_error():

            with patch('ipsum.util.logger.get_enviroment_variable') as mock_get_enviroment_variable:
            
                mock_get_enviroment_variable.return_value = logger.WARNING

                assert logger.error('error') is None

        _must_return_none_when_level_is_warning_and_log_is_error()

    def test_formmat_message(self):

        logger = Logger(self.TestClass())

        test_message = "Test!"

        expected_datetime = datetime.strftime(datetime.today(), "%d/%b/%Y %H:%M:%S")

        expected_message = f"[{expected_datetime}][{logger.INFO}] {self.TestClass}: {test_message}"

        assert expected_message == logger._format_message(test_message, logger.INFO)

    def test_info(self):

        with patch('ipsum.util.logger.get_enviroment_variable') as mock_get_enviroment_variable:
            
            logger = Logger(self.TestClass())            
            
            mock_get_enviroment_variable.return_value = logger.INFO

            assert logger.info('info') is not None

    def test_warning(self):

        with patch('ipsum.util.logger.get_enviroment_variable') as mock_get_enviroment_variable:
            
            logger = Logger(self.TestClass())            
            
            mock_get_enviroment_variable.return_value = logger.WARNING

            assert logger.warnning('warning') is not None

    def test_error(self):

        with patch('ipsum.util.logger.get_enviroment_variable') as mock_get_enviroment_variable:
            
            logger = Logger(self.TestClass())            
            
            mock_get_enviroment_variable.return_value = logger.ERROR

            assert logger.error('error') is not None
