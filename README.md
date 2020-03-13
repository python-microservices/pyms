# Python Microservices Library

[![PyPI version](https://badge.fury.io/py/py-ms.svg)](https://badge.fury.io/py/py-ms)
[![Build Status](https://travis-ci.org/python-microservices/pyms.svg?branch=master)](https://travis-ci.org/python-microservices/pyms)
[![Coverage Status](https://coveralls.io/repos/github/python-microservices/pyms/badge.svg?branch=master)](https://coveralls.io/github/python-microservices/pyms?branch=master)
[![Requirements Status](https://requires.io/github/python-microservices/pyms/requirements.svg?branch=master)](https://requires.io/github/python-microservices/pyms/requirements/?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/context:python)
[![Documentation Status](https://readthedocs.org/projects/py-ms/badge/?version=latest)](https://py-ms.readthedocs.io/en/latest/?badge=latest)
[![Gitter](https://img.shields.io/gitter/room/DAVFoundation/DAV-Contributors.svg)](https://gitter.im/python-microservices/pyms)


PyMS, Python MicroService, is a [Microservice chassis pattern](https://microservices.io/patterns/microservice-chassis.html) 
like Spring Boot (Java) or Gizmo (Golang). PyMS is a collection of libraries, best practices and recommended ways to build 
microservices with Python which handles cross-cutting concerns: 

- Externalized configuration
- Logging
- Health checks
- Metrics
- Distributed tracing

PyMS is powered by [Flask](https://flask.palletsprojects.com/en/1.1.x/), [Connexion](https://github.com/zalando/connexion) 
and [Opentracing](https://opentracing.io/).

Get started with [Installation](installation.md) and then get an overview with the [Quickstart](quickstart.md).

## Documentation

To know how use, install or build a project see the [docs](https://py-ms.readthedocs.io/en/latest/).

## Motivation

When we started to create microservice with no idea, we were looking for tutorials, guides, best practices, but we found
nothing to create professional projects. Most articles say:

- "Install flask"
- "Create routes"
- (Sometimes) "Create a swagger specs"
- "TA-DA! you have a microservice"

But... what happens with our configuration out of code like Kubernetes configmap? what happens with transactionality? 
If we have many microservices, what happens with traces?.

There are many problems around Python and microservices and we can`t find anyone to give a solution.

We start creating these projects to try to solve all the problems we have found in our professional lives about 
microservices architecture.

Nowadays, is not perfect and we have a looong roadmap, but we hope this library could help other fellas and friends ;) 

## Installation

```bash
pip install py-ms[all]
```

# Quickstart

You need to create 2 files: main.py and config.yml:

- **main.py**

```python
from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice() # 1.1
app = ms.create_app() # 2.1


@app.route("/") # 3.1
def example():
    return jsonify({"main": "hello world"})


if __name__ == '__main__':
    app.run()
```

- **config.yml**

```yaml
pyms:
  services: # 1.2
    requests:
      data: {}
  config: # 1.3
    DEBUG: true
    APP_NAME: business-glossary
    APPLICATION_ROOT : ""
    SECRET_KEY: "gjr39dkjn344_!67#"
```

### So what did that code do?

1. Create a instance of PyMS Microservice class (#1.1). This initialization inject the configuration defined in the
1.3 block and could be accessed through current_app.config like typical
[Flask config](https://flask.palletsprojects.com/en/1.1.x/config/).
Then, initialize the service defined in the 1.2 block. See [Services](services.md) for more details.

2. Initialize [Flask](https://flask.palletsprojects.com/en/1.1.x/) instance, [Connexion](https://github.com/zalando/connexion)
if it was defined in the pyms configuration block, create a tracer, add health-check blueprint, initialize libs and set
the PyMS Microservice in `ms` attribute and you can access to it with `current_app.ms`.  
This steps has their each functions and you can easy
override it.

3. `create_app` return the flask instance and you can interact with it as a typical flask app

See [Documentation](https://py-ms.readthedocs.io/en/latest/) to learn more.

## Create a project from scaffold

PyMS has a command line option to create a project template like [Microservices Scaffold](https://github.com/python-microservices/microservices-scaffold).
This command use [cookiecutter](https://github.com/cookiecutter/cookiecutter) to download and install this [template](https://github.com/python-microservices/microservices-template)

**[Warning]** You must run first `pip install cookiecutter==1.7.0`

```bash
pyms startproject
```

this output a lot of options step by step:

```bash
project_repo_url [https://github.com/python-microservices/microservices-scaffold]: 
project_name [Python Microservices Boilerplate]: example project
project_folder [example_project]: 
project_short_description [Python Boilerplate contains all the boilerplate you need to create a Python package.]: 
create_model_class [y]: 
microservice_with_swagger_and_connexion [y]: 
microservice_with_traces [y]: 
microservice_with_metrics [y]: 
application_root [/example_project]: 
Select open_source_license:
1 - MIT license
2 - BSD license
3 - ISC license
4 - Apache Software License 2.0
5 - GNU General Public License v3
6 - Not open source
Choose from 1, 2, 3, 4, 5, 6 [1]: 
```

When you finish to introduce the options, a project will be created in `[project_folder]` folder

## How To Contrib

We appreciate opening issues and pull requests to make PyMS even more stable & useful! See [This doc](CONTRIBUTING.md)
for more details.
