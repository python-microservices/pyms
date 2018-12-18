# Microservices class

The class Microservice is the core of all microservices built with PyMS. 


You can create a simple microservices like:

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

See more examples in TODO: add link