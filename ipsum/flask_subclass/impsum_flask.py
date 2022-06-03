
from flask import Flask
from ipsum.flask_subclass.ipsum_request import IpsumRequest


class IpsumFlask(Flask):

    request_class = IpsumRequest