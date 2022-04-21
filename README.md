Plugins utilizados:
- [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
- [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)
- [Bridge to Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.mindaro)
- [Kubernetes k3d](https://marketplace.visualstudio.com/items?itemName=inercia.vscode-k3d)

Link para utilizar clusters kubernetes no VSCode: [Working with Kubernetes in VS Code](https://code.visualstudio.com/docs/azure/kubernetes). Lembrando que ao utilizar o [k3d](https://k3d.io/) para criar seu cluster deve-se utilizar a extensão [Kubernetes k3d](https://marketplace.visualstudio.com/items?itemName=inercia.vscode-k3d).

Exemplo de Arquivo ```launch.json``` para criar debug em cluster kubernetes.

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

Exemplo de Arquivo ```tasks.json``` para criar debug em cluster kubernetes.

Lembre-se de alterar os seguintes parametrôs

**<:host>**              : URL do servidor. Ex: http://127.0.0.1

**<:port>**              : Porta do servidor. Ex: 5000

**<:db_user>**           : Usuário do banco de dados.

**<:db_password>**       : Senha para o banco de dados.

**<:atlas_prefix>**      : Prefixo da URL do Atlas Cluster. Ex: my-cluster.abcde.mongodb.net

**<:database_name>**     : Nome da base de dados.

**<:atlas_url_options>** : Opções do Atlas Cluster. Ex: retryWrites=true&w=majority

**<:isolated_container_name>** : Nome do container isolado. Ex: myname-f7bf


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
                    "TEST_MONGODB_USER": "<:db_user>",
                    "TEST_MONGODB_PASSWORD": "<:db_password>",
                    "TEST_MONGODB_ATLAS_PREFIX": "<:atlas_prefix>"
                    "TEST_MONGODB_DATABASE": "<:database_name>",
                    "TEST_MONGODB_URL_OPTIONS": "<:atlas_url_options>" 
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

Ambos os arquivos ficaram na pasta ```.vscode```.
