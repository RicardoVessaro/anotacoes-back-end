
from ipsum.exception.ipsum_exception import IpsumException, error_handler
from ipsum.ipsum_flask.ipsum_flask import IpsumFlask
from ipsum.service.enum.ipsum_enum import save_enums
from ipsum.util.enviroment_variable import get_database_url, get_test_database_url, is_test_enviroment
from ipsum.util.logger import Logger

class IpsumFlaskFactory:

    def __init__(self, name, database_object, blueprints) -> None:
        self.name = name
        self.database_object = database_object
        self.blueprints = blueprints
        
        self._logger = Logger(self)

        self.app = IpsumFlask(self.name)

        self._create_flask_app()

    def _create_flask_app(self):

        self._logger.info("Registering Error Handler...")
        self.app.register_error_handler(IpsumException, error_handler)

        self._set_database_config()

        self._register_blueprint()

        self._init_database()

        self._logger.info("Saving ENUMs...")
        save_enums()

    def _set_database_config(self):
        self._logger.info("Setting database...")
        MONGODB_HOST = self._get_database_config()

        self.app.config.update(**{"MONGODB_HOST": MONGODB_HOST})

    def _get_database_config(self):
        MONGODB_HOST = None

        if not is_test_enviroment():
            MONGODB_HOST = get_database_url()
        
        else:
            self._logger.info("     Using Test database...")
            MONGODB_HOST = get_test_database_url()
        
        return MONGODB_HOST

    def _register_blueprint(self):
        self._logger.info("Registering Blueprints...")

        for blueprint in self.blueprints:
            self._logger.info(f'    "{blueprint.name}" Blueprint')

            self.app.register_blueprint(blueprint)

    def _init_database(self):
        self._logger.info("Inniting database...")

        self.database_object.init_app(self.app)

    
