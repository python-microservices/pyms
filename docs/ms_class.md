# Microservices class

The class Microservice is the core of all microservices built with PyMS. 


You can create a simple microservice such as:

```python
from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice(service="my-minimal-microservice", path=__file__)
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({"main": "hello world"})


if __name__ == '__main__':
    app.run()
```

And a config file like this config.yml

```yaml
my-minimal-microservice:
  APP_NAME: "Python Microservice"
```
Check [Configuration](configuration.md) section to know how to create a configuration file.

Each keyword in our configuration block, can be accessed in our Microservice object through the attribute `config`.

```yaml
# Config.yml
example-config:
  APP_NAME: "Python Microservice"
  foo: "var"
  multiplevars:
    config1: "test1"
    config2: "test2"
  
```
```python
#app.py
from pyms.flask.app import Microservice

ms = Microservice(service="example-config", path=__file__)
print(ms.config.APP_NAME) 
# >> "Python Microservice"
print(ms.config.foo) 
# >> "bar"
print(ms.config.multiplevars.config1) 
# >> "test1"
print(ms.config.multiplevars.config2) 
# >> "test2"
```

Check more examples in [this Github page](https://github.com/python-microservices/pyms/tree/master/examples)