
# Flask Locally

To run flask locally first provide the following enviroment variables:

FLASK_APP: It defines de flask app of your application.
    
    export FLASK_APP=run.py


FLASK_ENV: It defines your flask enviroment

    export FLASK_ENV=development


FLASK_CONFIG: It defines de configuration path of your flask app.

    export FLASK_CONFIG=development.cfg

You can create other flask configs like FLASK_CONFIG_TEST to define other enviroment variables values.

    export FLASK_CONFIG_TEST=test.cfg

To run the application use:

    python -m run

To run the applicatin using other configuration use (for example FLASK_CONFIG_TEST):

    python -m run FLASK_CONFIG_TEST


To run the development enviroment you can use the script:

    source run-desenv.sh

To run the test enviroment you can use the script:

    source run-test.sh

Flask config file parameters.

```
# MongoDB 
MONGODB_USER = ""
MONGODB_PASSWORD = ""
MONGODB_DATABASE  = ""
MONGODB_ATLAS_PREFIX = ""
MONGODB_URL_OPTIONS = "

# Log
LOGGER_LEVEL = ""

# Integration Tests (don't set if is not a test enviroment)
INTEGRATION_TEST_HOST = ""
INTEGRATION_TEST_PORT = ""
```