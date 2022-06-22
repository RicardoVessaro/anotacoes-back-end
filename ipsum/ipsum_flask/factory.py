
from ipsum.exception.ipsum_exception import IpsumException, error_handler
from ipsum.ipsum_flask.ipsum_flask import IpsumFlask
from ipsum.service.enum.ipsum_enum import save_enums
from ipsum.util.enviroment_variable import get_database_url, set_config_variables
from ipsum.util.logger import Logger

class IpsumFlaskFactory:

    def __init__(self, name, database_object, blueprints, config_env_var='FLASK_CONFIG') -> None:
        self.name = name
        self.database_object = database_object
        self.blueprints = blueprints
        
        self._logger = Logger(self)

        self.app = IpsumFlask(self.name)

        self.app.config.from_envvar(config_env_var, silent=True)

        set_config_variables(self.app.config.get_namespace('', lowercase=False))

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
        MONGODB_HOST = get_database_url()
        
        return MONGODB_HOST

    def _register_blueprint(self):
        self._logger.info("Registering Blueprints...")

        for blueprint in self.blueprints:
            self._logger.info(f'    "{blueprint.name}" Blueprint')

            self.app.register_blueprint(blueprint)

    def _init_database(self):
        self._logger.info("Initing database...")

        self.database_object.init_app(self.app)

    
