
# Ambiente

## Flask Locally

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

---

## Application debug using VSCode

Used extensions:
- [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
- [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)
- [Bridge to Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.mindaro)
- [Kubernetes k3d](https://marketplace.visualstudio.com/items?itemName=inercia.vscode-k3d)

Link to use kubernetes in VSCode: [Working with Kubernetes in VS Code](https://code.visualstudio.com/docs/azure/kubernetes). Remember, if you use [k3d](https://k3d.io/) to create your cluster you must use [Kubernetes k3d](https://marketplace.visualstudio.com/items?itemName=inercia.vscode-k3d) extension.

Remember to change the following parameters

**<:host>**              : Server URL. Ex: http://127.0.0.1

**<:port>**              : Server port. Ex: 5000

**<:file.cfg>**          : `.cfg` file used to define flask configuration. There are others enviroment variables to use besides FLASK_CONFIG, like FLASK_CONFIG_TEST.

**<:db_user>**           : Database user.

**<:db_password>**       : Databases password.

**<:atlas_prefix>**      : Atlas Cluster URL prefix. Ex: my-cluster.abcde.mongodb.net

**<:database_name>**     : Database name.

**<:atlas_url_options>** : Atlas Cluster options. Ex: retryWrites=true&w=majority

**<:isolated_container_name>** : Isolated container name for kubernetes. Ex: myname-f7bf

**<:log_level>** : Application log level (INFO, WARNING, ERROR).

### Configuration Examples.

### LOCAL

```launch.json``` file example to debug locally.

```
{
    "name": "Desenv: Python Flask",
    "type": "python",
    "request": "launch",
    "module": "run",
    "env": {
        "FLASK_APP": "run.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "0",
        "FLASK_CONFIG": "<:file>.cfg",
        "MONGODB_USER": "<:db_user>",
        "MONGODB_PASSWORD": "<:atlas_prefix>",
        "MONGODB_DATABASE": "<:database_name>",
        "MONGODB_ATLAS_PREFIX": "<:atlas_prefix>",
        "MONGODB_URL_OPTIONS": "<:atlas_url_options>",
        "LOGGER_LEVEL": "<:log_level>"
    },
    "args": [],
    "jinja": true
}
```

```launch.json``` file example to test locally (Remeber to run the application first). 

```
{
    "name": "Run tests: Python Flask",
    "type": "python",
    "request": "launch",
    "module": "pytest",
    "env": {
        "MONGODB_USER": "<:db_user>",
        "MONGODB_PASSWORD": "<:atlas_prefix>",
        "MONGODB_DATABASE": "<:database_name>",
        "MONGODB_ATLAS_PREFIX": "<:atlas_prefix>",
        "MONGODB_URL_OPTIONS": "<:atlas_url_options>",
        "LOGGER_LEVEL": "<:log_level>"
        "INTEGRATION_TEST_HOST": "<:host>",
        "INTEGRATION_TEST_PORT": "<:port>"
    },
    "args": [
        "-p",
        "no:cacheprovider"
    ]
}
```

### KUBERNETES CLUSTER

To kubernetes cluster we use to files ```launch.json``` and ```tasks.json```.

```launch.json``` file example to debug in kubernetes cluster.

```$json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Docker: Python - Flask with Kubernetes",
            "type": "docker",
            "request": "launch",
            "preLaunchTask": "bridge-to-kubernetes.compound",
            "python": {
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}",
                        "remoteRoot": "/app"
                    }
                ],
                "projectType": "flask"
            },
            "env": {
                "GRPC_DNS_RESOLVER": "native"
            }
        },
        {
            "name": "Docker: Python - Flask",
            "type": "docker",
            "request": "launch",
            "preLaunchTask": "docker-run: debug",
            "python": {
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}",
                        "remoteRoot": "/app"
                    }
                ],
                "projectType": "flask"
            }
        }
    ]
}
```

```tasks.json``` file example to debug in kubernetes cluster.

```$json
{
	"version": "2.0.0",
	"tasks": [
		{
			"type": "docker-build",
			"label": "docker-build",
			"platform": "python",
			"dockerBuild": {
				"dockerfile": "${workspaceFolder}/Dockerfile",
				"context": "${workspaceFolder}",
				"tag": "ricardovessaro/anotacoes-back-end:debug",
				"pull": true
			}
		},
		{
			"type": "docker-run",
			"label": "docker-run: debug",
			"dependsOn": [
				"docker-build"
			],
			"dockerRun": {
				"containerName": "container-anotacoes-back-end",
				"image": "ricardovessaro/anotacoes-back-end:debug",
				"remove": true,
				"env": {
					"FLASK_ENV": "development",
					"INTEGRATION_TEST_HOST": "<:host>",
                    "INTEGRATION_TEST_PORT": "<:port>",
                    "MONGODB_USER": "<:db_user>",
                    "MONGODB_PASSWORD": "<:db_password>",
                    "MONGODB_ATLAS_PREFIX": "<:atlas_prefix>"
                    "MONGODB_DATABASE": "<:database_name>",
                    "MONGODB_URL_OPTIONS": "<:atlas_url_options>" 
				},
				"volumes": [
					{
						"containerPath": "/app",
						"localPath": "${workspaceFolder}"
					}
				],
				"ports": [
					{
						"containerPort": 5000,
						"hostPort": 5001
					}
				]
			},
			"python": {
				"args": [
					"run",
					"--host",
					"0.0.0.0",
					"--port",
					"5000"
				],
				"module": "flask"
			}
		},
		{
			"label": "bridge-to-kubernetes.resource",
			"type": "bridge-to-kubernetes.resource",
			"resource": "anotacoes-back-end",
			"resourceType": "service",
			"ports": [
				5001
			],
			"targetCluster": "k3d-anotacoes-cluster",
			"targetNamespace": "default",
			"useKubernetesServiceEnvironmentVariables": false,
			"isolateAs": "<:isolated_container_name>"
		},
		{
			"label": "bridge-to-kubernetes.compound",
			"dependsOn": [
				"bridge-to-kubernetes.resource",
				"docker-run: debug"
			],
			"dependsOrder": "sequence"
		}
	]
}
```

All the files must be in ```.vscode``` folder.

---

### RUN TESTS IN KUBERNETES
Use the remote explorer to attach to container.

After connect to the container go do 'app' file.

    cd ../../app

To run the tests use:

    python3 -m pytest -p no:cacheprovider
