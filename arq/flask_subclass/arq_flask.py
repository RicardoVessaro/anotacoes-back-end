
from flask import Flask
from arq.flask_subclass.arq_request import ArqRequest


class ArqFlask(Flask):

    request_class = ArqRequest