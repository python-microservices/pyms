# Microservices class

The class Microservice is the core of all microservices built with PyMS. 


You can create a simple microservice such as:

```python
from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice(path=__file__)
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({"main": "hello world"})


if __name__ == '__main__':
    app.run()
```

And a config file like this config.yml

```yaml
pyms:
	config:
  	APP_NAME: "Python Microservice"
```
Check [Configuration](configuration.md) section to know how to create a configuration file.

`Microservice` class search for a `config.yml` in the directory you pass in `path` parameter or search the file in
`CONFIGMAP_FILE` env var.

Each keyword in our configuration block, can be accessed in our Microservice object through the attribute `config`.

```yaml
# Config.yml
pyms:
  config:
    app_name: "Python Microservice"
      foo: "var"
        multiplevars:
          config1: "test1"
          config2: "test2"
  
```
```python
#app.py
from pyms.flask.app import Microservice

ms = Microservice(path=__file__)
print(ms.config.APP_NAME) 
# >> "Python Microservice"
print(ms.config.app_name) 
# >> "Python Microservice"
print(ms.config.foo) 
# >> "bar"
print(ms.config.multiplevars.config1) 
# >> "test1"
print(ms.config.multiplevars.config2) 
# >> "test2"
```

## Personalize your microservices

Microservice class initialize the libraries and other process by this way:

```python
		...
    def create_app(self):
        """Initialize the Flask app, register blueprints and initialize
        all libraries like Swagger, database,
        the trace system...
        return the app and the database objects.
        :return:
        """
        self.application = self.init_app()
        self.application.config.from_object(self.config)
        self.application.tracer = None
        self.application.ms = self

        # Initialize Blueprints
        self.application.register_blueprint(healthcheck_blueprint)

        self.init_libs()
        self.add_error_handlers()

        self.init_tracer()

        self.init_logger()

        return self.application
```

Create a class that inherit from `pyms.flask.app.Microservice` and create and override methods with your own configuration.
The next example show how to create your own logger and innit a lib like [Flask Babel](https://pythonhosted.org/Flask-Babel/)

```python
class MyMicroservice(Microservice):
    def init_tracer(self):
        pass # Disabled tracer

    def init_libs(self):
        babel = Babel(self.application)

        return self.application

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



Check more examples in [this Github page](https://github.com/python-microservices/pyms/tree/master/examples)