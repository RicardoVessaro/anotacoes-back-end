
from flask import Flask
from arq.flask_subclass.ipsum_request import IpsumRequest


class IpsumFlask(Flask):

    request_class = IpsumRequest