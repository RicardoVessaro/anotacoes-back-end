
from flask import Flask
from ipsum.ipsum_flask.ipsum_request import IpsumRequest

class IpsumFlask(Flask):

    request_class = IpsumRequest
