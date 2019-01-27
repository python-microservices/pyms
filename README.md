# Python Microservices Library

[![PyPI version](https://badge.fury.io/py/py-ms.svg)](https://badge.fury.io/py/py-ms)
[![Build Status](https://travis-ci.org/python-microservices/pyms.svg?branch=master)](https://travis-ci.org/python-microservices/pyms)
[![Coverage Status](https://coveralls.io/repos/github/python-microservices/pyms/badge.svg?branch=master)](https://coveralls.io/github/python-microservices/pyms?branch=master)
[![Requirements Status](https://requires.io/github/python-microservices/pyms/requirements.svg?branch=master)](https://requires.io/github/python-microservices/pyms/requirements/?branch=master)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/python-microservices/pyms.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/python-microservices/pyms/context:python)

PyMS, Python MicroService, is a collections of libraries, best practices and recommended ways to build 
microservices with Python.

To know how use, install or build a project see the docs: https://py-ms.readthedocs.io/en/latest/

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

## Pipenv

### Advantages over plain pip and requirements.txt
[Pipenv](https://pipenv.readthedocs.io/en/latest/) generates two files: a `Pipfile`and a `Pipfile.lock`.
* `Pipfile`: Is a high level declaration of the dependencies of your project. It can contain "dev" dependencies (usually test related stuff) and "standard" dependencies which are the ones you'll need for your project to function
* `Pipfile.lock`: Is the "list" of all the dependencies your Pipfile has installed, along with their version and their hashes. This prevents two things: Conflicts between dependencies and installing a malicious module.

### How to...

Here the most 'common' `pipenv` commands, for a more in-depth explanation please refer to  the [official documentation](https://pipenv.readthedocs.io/en/latest/).

#### Install pipenv
```bash
pip install pipenv
```

#### Install dependencies defined in a Pipfile
```bash
pipenv install
```

#### Install both dev and "standard" dependencies defined in a Pipfile
```bash
pipenv install --dev
```

#### Install a new module
```bash
pipenv install django
```

#### Install a new dev module (usually test related stuff)
```bash
pipenv install nose --dev
```

#### Install dependencies in production
```bash
pipenv install --deploy
```

#### Start a shell
```bash
pipenv shell
```

## Documentation

This project use MkDocs

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

### Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

