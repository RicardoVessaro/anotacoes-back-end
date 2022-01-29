from api.api import create_flask_app

api = create_flask_app()


@api.route("/")
def root():
    return "API esta rodando !!!"

if __name__=='__main__':
    api.run()