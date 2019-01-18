# Configuration

Each microservice needs a config file in yaml or json format to work with it. This configuration contains
the Flask settings of your project and the [Services](services.md).

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
