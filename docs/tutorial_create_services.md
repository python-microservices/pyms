# Tutorial 2: How To contribute, Create your own service

* First, you must create a file with the name of your service inside of `pyms.flask.service`, for example, 
"myawesomesrv":

pyms/flask/services/myawesomesrv.py
```python
from pyms.flask.services.driver import DriverService


class Service(DriverService):
    service = "myawesomesrv"
    default_values = {
        "myvalue": 0,
        "myvalue2": 1
    }
```

* Now, you can configure your service from `config.yml`
```yaml
pyms:
  config:
    myawesomesrv:
      myvalue: 5
```

* Your service will be instanced inside the `ms` object in `flask.current_app` object. For example, with the last config,
you could print the folowing code:

```python
from flask import jsonify, current_app

from pyms.flask.app import Microservice

ms = Microservice(service="my-minimal-microservice", path=__file__)
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({
    	"myvalue": current_app.ms.myawesomesrv.myvalue, 
    	"myvalue2": current_app.ms.myawesomesrv.myvalue2
    })


if __name__ == '__main__':
    app.run()
```

This would be the output in `http://localhost:5000/`:

```json
{"myvalue": 5, "myvalue2": 1}
```