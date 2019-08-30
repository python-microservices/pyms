# Configuration

## Create configuration
Each microservice needs a config file in yaml or json format to work with it. This configuration contains
the Flask settings of your project and the [Services](services.md). With this way to create configuration files, we 
solve two problems of the [12 Factor apps](https://12factor.net/):
- Store config out of the code
- Dev/prod parity: the configuration could be injected and not depends of our code, for example, Kubernetes config maps

a simple configuration file could be a config.yaml:

```yaml
pyms:
  requests: true
  swagger:
    path: ""
    file: "swagger.yaml"
my-ms:
  DEBUG: true
  TESTING: false
  APP_NAME: "Python Microservice"
  APPLICATION_ROOT: ""
```

or in a config.json:

```json
{
"pyms":{
  "requests": true,
  "swagger": {
    "path": "",
    "file": "swagger.yaml"
    }
  },
"my-ms": {
  "DEBUG": true,
  "TESTIN": false,
  "APP_NAME": "Python Microservice",
  "APPLICATION_ROOT": ""
  }
}
```

This file could contains this keywords:


## pyms block

```pyms```: all subsets inside this keyword are the settings of this library. Each keyword will be a service of our
[Microservice class](ms_class.md). For example, we declare our microservice class as:

```python
from pyms.flask.app import Microservice
ms = Microservice(service="my-ms", path=__file__)
```
and a `config.yaml` file:

```yaml
pyms:
  requests: true
```

our object `ms` has an attribute `requests` that is a instance of our service [requests](services.md). 

## Our microservice block
This part contains all keywords of a [Flask Configuration Handling](http://flask.pocoo.org/docs/1.0/config/) and our 
constants of the enviroments (local configuration, staging configuration...). Keep in mind that a Flask configuration needs
the keywords to be declared as uppercase.

The name of this block is defined when you create the object of [Microservice class](ms_class.md):

### Example 1
```python
from pyms.flask.app import Microservice
ms = Microservice(service="my-personal-microservice", path=__file__)
```
and a `config.yaml` file:

```yaml
my-personal-microservice:
  DEBUG: true
  TESTING: false
```

### Example 2
```python
from pyms.flask.app import Microservice
ms = Microservice(service="ms1-api", path=__file__)
```
and a `config.yaml` file:

```yaml
ms1-api:
  DEBUG: true
  TESTING: false
```

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

**IMPORTANT:** If you use this method to get configuration out of context, you must set the `CONFIGMAP_SERVICE` or set 
the default key `ms` for your configuration block in your config.yml