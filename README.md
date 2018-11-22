# Python Microservices Library

[![PyPI version](https://badge.fury.io/py/py-ms.svg)](https://badge.fury.io/py/py-ms)
[![Build Status](https://travis-ci.org/python-microservices/pyms.svg?branch=master)](https://travis-ci.org/python-microservices/pyms)
[![Coverage Status](https://coveralls.io/repos/github/python-microservices/pyms/badge.svg?branch=master)](https://coveralls.io/github/python-microservices/pyms?branch=master)
[![Requirements Status](https://requires.io/github/python-microservices/pyms/requirements.svg?branch=master)](https://requires.io/github/python-microservices/pyms/requirements/?branch=master)
[![Updates](https://pyup.io/repos/github/python-microservices/pyms/shield.svg)](https://pyup.io/repos/github/python-microservices/pyms/)
[![Python 3](https://pyup.io/repos/github/python-microservices/pyms/python-3-shield.svg)](https://pyup.io/repos/github/python-microservices/pyms/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/context:python)


## Installation 
```bash
pip install py-ms
```

## Structure

### pyms/config
Module to read yaml or json configuration from a dictionary or a path.

### pyms/flask/app
With the funcion `create_app` initialize the Flask app, register [blueprints](http://flask.pocoo.org/docs/0.12/blueprints/)
and intialize all libraries like Swagger, database, trace system, custom logger format, etc.

### pyms/flask/healthcheck
This views is usually used by Kubernetes, Eureka and other systems to check if our application is up and running.

### pyms/logger
Print logger in JSON format to send to server like Elasticsearch. Inject span traces in logger.

### pyms/rest_template
Encapsulate common rest operations between business services propagating trace headers if configured.

### pyms/tracer
Create an injector `flask_opentracing.FlaskTracer` to use in our projects
