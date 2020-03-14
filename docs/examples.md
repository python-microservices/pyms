# Examples

## Example 1: Basic Example

```bash
pip install py-ms[all]
```

config.yml:

```yaml
pyms:
  config:
    app_name: "Python Microservice"
```

main.py

```python
from flask import jsonify, current_app

from pyms.flask.app import Microservice

ms = Microservice()
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({"main": "hello world {}".format(current_app.config["APP_NAME"])})


if __name__ == '__main__':
    app.run()
```

```bash
python main.py
```

Open in your browser http://localhost:5000/

## Example 2: Create your Microservice class

Create a class that inherit from `pyms.flask.app.Microservice` and override methods with your own configuration.
The next example show how to innit a lib like [Flask Babel](https://pythonhosted.org/Flask-Babel/)

main.py:

```python
from flask_babel import Babel
from pyms.flask.app import Microservice

class MyMicroservice(Microservice):
    def init_libs(self):
        babel = Babel(self.application)

        return self.application
        
ms = MyMicroservice()
app = ms.create_app()
```

## Example 2: Initialize SQLAlchemy

The next example show how to innit a lib like [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

config.yml:

```yaml
pyms:
  config:
    DEBUG: true
    APP_NAME: MyDB
    APPLICATION_ROOT: ""
    SQLALCHEMY_DATABASE_URI: mysql+mysqlconnector://user:pass@0.0.0.0/myschema
```
main.py:

```python
from flask_sqlalchemy import SQLAlchemy
from pyms.flask.app import Microservice

DB = SQLAlchemy()


class MyMicroservice(Microservice):
    def init_libs(self):
        self.application.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            'pool_size': 10,
            'pool_recycle': 120,
            'pool_pre_ping': True
        }
        DB.init_app(self.application)

ms = MyMicroservice()
app = ms.create_app()
```

## Example 3: Create your logger

The next example show how to create a personal logger for your application

```python
import logging.config

from pyms.flask.app import Microservice


class MyMicroservice(Microservice):
    def init_logger(self):
        level = "INFO"
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'console': {
                    'format': '[%(asctime)s][%(levelname)s] %(name)s '
                              '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
                    'datefmt': '%H:%M:%S',
                },
            },
            'handlers': {
                'console': {
                    'level': level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'console'
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console'],
                    'level': level,
                    'propagate': True,
                },
                'root': {
                    'handlers': ['console'],
                    'level': level,
                    'propagate': True,
                },
            }
        }
        logging.config.dictConfig(LOGGING)

ms = MyMicroservice(path=__file__)
app = ms.create_app()
```

See [this Github page](https://github.com/python-microservices/pyms/tree/master/examples) to see a examples