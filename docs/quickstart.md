# Quickstart

This page gives a good introduction to PyMS. It assumes you already have PyMS installed. If you do not, head over to the [Installation](installation.md) section.

You need to create 2 files: main.py and config.yml:

main.py
```python
from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice(path=__file__) # 1.1
app = ms.create_app() # 2.1


@app.route("/") # 3.1
def example():
    return jsonify({"main": "hello world"})


if __name__ == '__main__':
    app.run()
```

config.yml
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

## So what did that code do?

1. Create a instance of PyMS Microservice class (#1.1). This initialization inject the configuration defined in the 
1.3 block and could be accessed through current_app.config. Then, initialize the service defined in the 1.2 block. See [Services](services.md) for more details.
2. Initialize [Flask](https://flask.palletsprojects.com/en/1.1.x/) instance, [Connexion](https://github.com/zalando/connexion) 
if it was defined in the pyms configuration block, create a tracer, add health-check blueprint, initialize libs and set the PyMS Microservice in
`ms` attribute and you can access to it with `current_app.ms`. This steps has their each functions and you can easy override it.
3. `create_app` return the flask instance and you can interact with it as a typical flask app

# Create a project from scaffold

PyMS have a command line option to create a project template like [Microservices Scaffold](https://github.com/python-microservices/microservices-scaffold).
This command use [cookiecutter](https://github.com/cookiecutter/cookiecutter) to download and install this [template](https://github.com/python-microservices/microservices-template)

!!! warning
    You must run first `pip install cookiecutter==1.7.0`

## Installation

```bash
pyms startproject
`
``

this output a lot of options step by step 

```bash
project_repo_url [https://github.com/python-microservices/microservices-scaffold]: 
project_name [Python Microservices Boilerplate]: prueba descarga
project_folder [prueba_descarga]: 
project_short_description [Python Boilerplate contains all the boilerplate you need to create a Python package.]: 
create_model_class [y]: 
microservice_with_swagger_and_connexion [y]: 
microservice_with_traces [y]: 
microservice_with_metrics [y]: 
application_root [/prueba_descarga]: 
Select open_source_license:
1 - MIT license
2 - BSD license
3 - ISC license
4 - Apache Software License 2.0
5 - GNU General Public License v3
6 - Not open source
Choose from 1, 2, 3, 4, 5, 6 [1]: 
```

When you finish to introduce the options, a project will be created in `[project_slug]` folder

See [Configuration](configuration.md), [Routing](routing.md) and [Examples](examples.md) to continue with this tutorial