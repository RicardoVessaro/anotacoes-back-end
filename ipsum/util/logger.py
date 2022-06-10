
from datetime import datetime
from ipsum.util.enviroment_variable import LOGGER_LEVEL, get_enviroment_variable


class Logger:

    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    levels = [INFO, WARNING, ERROR]

    _info_level = [INFO]
    _warnning_level = _info_level + [WARNING]
    _error_level = _warnning_level + [ERROR]

    _DATE_FORMAT = "%d/%b/%Y %H:%M:%S"

    def __init__(self, log_class) -> None:
        self.log_class = log_class

    def info(self, message):
        return self._log(message, self.INFO)

    def warnning(self, message):
        return self._log(message, self.WARNING)

    def error(self, message):
        return self._log(message, self.ERROR)

    def class_name(self):
        return str(self.log_class.__class__)

    def levels(self):
        level = get_enviroment_variable(LOGGER_LEVEL)
        
        if level == self.INFO:
            return self._info_level
        
        elif level == self.WARNING:
            return self._warnning_level

        elif level == self.ERROR:
            return self._error_level

        else:
            return None

    def _log(self, message, level):
        levels = self.levels()

        if levels is not None and level in levels:
            formatted_message = self._format_message(message, level)

            print(formatted_message)

            return formatted_message

        return None

    def _format_message(self, message, level):
        str_datetime = datetime.strftime(datetime.today(), self._DATE_FORMAT)

        return f'[{str_datetime}][{level}] {self.class_name()}: {message}'
    