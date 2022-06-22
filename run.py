import sys
from flask import request
from api.api import create_flask_app

config_env_var = sys.argv[1] if len(sys.argv) > 1 else 'FLASK_CONFIG'
api = create_flask_app(config_env_var)



@api.route("/")
def root():
    return f"API esta rodando em {request.host_url}"

if __name__=='__main__':
    api.run()