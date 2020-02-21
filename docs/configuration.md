# Configuration

## Environments variables of PyMS:

**CONFIGMAP_FILE**: The path to the configuration file. By default, PyMS search the configuration file in your
actual folder with the name "config.yml"
**KEY_FILE**: The path to the key file to decrypt your configuration. By default, PyMS search the configuration file in your
actual folder with the name "key.key"

## Create configuration
Each microservice needs a config file in yaml or json format to work with it. This configuration contains
the Flask settings of your project and the [Services](services.md). With this way to create configuration files, we 
solve two problems of the [12 Factor apps](https://12factor.net/):

- Store config out of the code
- Dev/prod parity: the configuration could be injected and not depends of our code, for example, Kubernetes configmaps

a simple configuration file could be a config.yaml:

```yaml
pyms:
  services:
    requests: true
    swagger:
      path: ""
      file: "swagger.yaml"
  config:
    debug: true
    testing: false
    app_name: "Python Microservice"
    APPLICATION_ROOT: ""
```

or in a config.json:

```json
{
  "pyms": {
    "services":{
      "requests": true,
      "swagger": {
        "path": "",
        "file": "swagger.yaml"
      }
    },
    "config": {
      "DEBUG": true,
      "TESTING": true,
      "APP_NAME": "Python Microservice",
      "APPLICATION_ROOT": "/",
      "test_var": "general",
      "subservice1": {
        "test": "input"
      },
      "subservice2": {
        "test": "output"
      }
    }
  }
}
```

This file could contains this keywords:

## pyms - services block

```pyms```: all subsets inside this keyword are the settings of this library. Each keyword will be a service of our
[Microservice class](ms_class.md). For example, we declare our microservice class as:

```python
from pyms.flask.app import Microservice
ms = Microservice(path=__file__)
```
and a `config.yaml` file:

```yaml
pyms:
  services:
    requests: true
```

our object `ms` has an attribute `requests` that is a instance of our service [requests](services.md). 

## pyms - config block
This part contains all keywords of a [Flask Configuration Handling](http://flask.pocoo.org/docs/1.0/config/) and our 
constants of the enviroments (local configuration, staging configuration...). Keep in mind that a Flask configuration needs
the keywords to be declared as uppercase. If you defined a variable like `app_name`, you will get this with 
`current_app.config["APP_NAME"]`


## Import Configuration
With pyms, all configuration is stored as flask configuration and it can be acceded from:

```python
from flask import current_app; 

def my_endpoint():
	print(current_app.config["DEBUG"])
```

But, what happend if you need the configuration BEFORE Flask class is instanced? Imagine this case:

```python
from flask import Blueprint, current_app
from flask_restplus import Api

my_api_blueprint = Blueprint('api', __name__)

API = Api(
    my_api_blueprint,
    title='My Microservice',
    version=current_app.config["APP_VERSION"],
    description='Microservice to manage hierarchies',
    add_specs=True,
)
```

This raise a `'working outside of application context` error. Who can solve this problem?

```python
from flask import Blueprint, current_app
from flask_restplus import Api
from pyms.flask.app import config

my_api_blueprint = Blueprint('api', __name__)

API = Api(
    my_api_blueprint,
    title='My Microservice',
    version=config().APP_VERSION,
    description='Microservice to manage hierarchies',
    add_specs=True,
)
```


## Looking for Configuration file with Kubernetes Configmaps
By default, Microservice class search a config.yml in the same path. You can set a different route or set a json file.
To change this path, define a environment variable `CONFIGMAP_FILE`.

This way of looking for the configuration is useful when you work with Docker and Kubernetes. For example, you can integrate
a configmap of Kubernetes, with this microservice and a deployment with:

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: my-microservice
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: my-microservice
        image: ...
        env:
          - name: CONFIGMAP_FILE
            value: "/usr/share/microservice/config.yaml"

        volumeMounts:
          - mountPath: /usr/share/microservice
            name: ms-config-volume
      volumes:
        - name: ms-config-volume
          configMap:
            name: my-microservice-configmap
```

See [Routing](routing.md) and [Examples](examples.md) to continue with this tutorial