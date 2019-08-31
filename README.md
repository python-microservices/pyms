# Python Microservices Library

[![PyPI version](https://badge.fury.io/py/py-ms.svg)](https://badge.fury.io/py/py-ms)
[![Build Status](https://travis-ci.org/python-microservices/pyms.svg?branch=master)](https://travis-ci.org/python-microservices/pyms)
[![Coverage Status](https://coveralls.io/repos/github/python-microservices/pyms/badge.svg?branch=master)](https://coveralls.io/github/python-microservices/pyms?branch=master)
[![Requirements Status](https://requires.io/github/python-microservices/pyms/requirements.svg?branch=master)](https://requires.io/github/python-microservices/pyms/requirements/?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/context:python)

PyMS, Python MicroService, is a collections of libraries, best practices and recommended ways to build 
microservices with Python.

## Documentation

To know how use, install or build a project see the docs: https://py-ms.readthedocs.io/en/latest/

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

Nowadays, is not perfect and we have a looong roadmap, but we hope this library could help other felas and friends ;) 


## Installation 
```bash
pip install py-ms
```

## Structure

### pyms/config
Module to read yaml or json configuration from a dictionary or a path.

### pyms/flask/app
With the function `create_app` initialize the Flask app, register [blueprints](http://flask.pocoo.org/docs/0.12/blueprints/)
and initialize all libraries such as Swagger, database, trace system, custom logger format, etc.

### pyms/flask/services
Integrations and wrappers over common libs like request, swagger, connexion

### pyms/flask/healthcheck
This view is usually used by Kubernetes, Eureka and other systems to check if our application is running.

### pyms/logger
Print logger in JSON format to send to server like Elasticsearch. Inject span traces in logger.

### pyms/tracer
Create an injector `flask_opentracing.FlaskTracer` to use in our projects.

## How To Contrib
We appreciate opening issues and pull requests to make PyMS even more stable & useful! See [This doc](COONTRIBUTING.md)
for more details