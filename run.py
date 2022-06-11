from flask import request
from api.api import create_flask_app

api = create_flask_app()


@api.route("/")
def root():
    return f"API esta rodando em {request.host_url}"

if __name__=='__main__':
    api.run()