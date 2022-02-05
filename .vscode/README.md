Plugins utilizados:
- [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
- [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)
- [Bridge to Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.mindaro)
- [Kubernetes k3d](https://marketplace.visualstudio.com/items?itemName=inercia.vscode-k3d)

Link para utilizar clusters kubernetes no VSCode: [Working with Kubernetes in VS Code](https://code.visualstudio.com/docs/azure/kubernetes). Lembrando que ao utilizar o [k3d](https://k3d.io/) para criar seu cluster deve-se utilizar a extensão [Kubernetes k3d](https://marketplace.visualstudio.com/items?itemName=inercia.vscode-k3d).

Exemplo de Arquivo ```launch.json``` para criar debug em cluster kubernetes.

```$yaml

{
    "version": "0.2.0",
    "configurations": [
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

```$yaml

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
					"FLASK_ENV": "development"
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
	]
}

```

Ambos os arquivos ficaram na pasta ```.vscode```.
