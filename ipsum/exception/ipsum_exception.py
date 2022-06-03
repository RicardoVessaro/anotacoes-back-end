
import traceback

from flask import make_response
from ipsum.util.view.view_encoder import ViewEncoder

def error_handler(exception):
    response = ViewEncoder().default(exception.to_dict())

    return make_response(response, exception.status_code)

class IpsumException(Exception):

    BAD_REQUEST = 400

    def __init__(self, message, payload=None, status_code=BAD_REQUEST) -> None:
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error = dict(self.payload or ())
        error['message'] = self.message
        error['status_code'] = self.status_code
        error['stacktrace'] = traceback.format_exc()

        return error

