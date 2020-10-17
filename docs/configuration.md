# Configuration

## Environments variables of PyMS:

**PYMS_CONFIGMAP_FILE**: The path to the configuration file. By default, PyMS searches for the configuration file in your
current folder with the name "config.yml"
**PYMS_KEY_FILE**: The path to the key file to decrypt your configuration. By default, PyMS searches for the configuration file in your
current folder with the name "key.key"

## Create configuration
Each microservice needs a config file in yaml or json format for it to work with. This configuration contains
the Flask settings of your project and the [Services](services.md). With this way of creating configuration files, we 
solve two problems of the [12 Factor apps](https://12factor.net/):

- Store config out of the code
- Dev/prod parity: the configuration could be injected and doesn't depend on our code, for example, Kubernetes configmaps

A simple configuration file could be a config.yaml:

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

This file can contain the following keywords:

## pyms - services block

```pyms```: all subsets inside this keyword are the settings of this library. Each keyword will be a service of our
[Microservice class](ms_class.md). For example, if we declare our microservice class as:

```python
from pyms.flask.app import Microservice
ms = Microservice(path=__file__)
```
and have a `config.yaml` file such as:

```yaml
pyms:
  services:
    requests: true
```

our `ms` object will have an attribute `requests` that is a instance of our service [requests](services.md). 

## pyms - config block
This section contains all keywords used for general [Flask Configuration Handling](http://flask.pocoo.org/docs/1.0/config/), along 
with our constants for the different enviroments (local configuration, staging configuration...). Keep in mind that 
a Flask app configuration needs the keywords to be declared as uppercase. If you defined a variable like `app_name`, 
you will be able to retrieve it with `current_app.config["APP_NAME"]`


## Import Configuration
With pyms, all configuration is stored as flask configuration and it can be acceded from:

```python
from flask import current_app; 

def my_endpoint():
	print(current_app.config["DEBUG"])
```

But, what happens if you need to access the configuration BEFORE Flask class is instanced? Imagine this case:

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

This raises a `'working outside of application context` error. Who can solve this problem?

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
By default, the Microservice class searches for a config.yml in the same path. You can set a different route or set a json file.
To change this path, you must define an environment variable called `PYMS_CONFIGMAP_FILE`.

This way of looking for the configuration is useful when you work with Docker and Kubernetes. For example, you could integrate
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
          - name: PYMS_CONFIGMAP_FILE
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

## Reload configuration without stopping your services

In a production environment you may need to change the microservice's configuration without restarting it.

PyMS has a feature to reload the configuration:

```
curl -X POST http://localhost:5000/reload-config
```

This endpoint calls the method `Microservice.reload_conf()`, which restarts the services, 
the encryption configuration and initializes `create_app`.

```python
    def reload_conf(self):
        self.delete_services()
        self.config.reload()
        self.services = []
        self.init_services()
        self.crypt.config.reload()
        self.create_app()
```

This means that your libraries will be restarted, which is why it's important to initialize your BD, 
your configuration inside `init_libs` method. See more info [how to use Microservice class in this link](ms_class.md)
