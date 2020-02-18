# Services

Services are libraries, resources and extensions added to the Microservice in the configuration file.
This services are created as an attribute of the [Microservice class](ms_class.md) to use in the code.

To add a service check the [configuration section](configuration.md).

You can declare a service but activate/deactivate with the keyword `enabled`, like:

```yaml
pyms:
  services:
    requests:
      enabled: false
```

Current services are:

## Swagger / connexion

Extends the Microservice with [Connexion](https://github.com/zalando/connexion) and [swagger-ui](https://github.com/sveint/flask-swagger-ui).

### Configuration

The parameters you can add to your config are:

* **path:** The relative or absolute route to your swagger yaml file. The default value is the current directory
* **file:** The name of you swagger yaml file. The default value is `swagger.yaml`
* **url:** The url where swagger run in your server. The default value is `/ui/`.
* **project_dir:** Relative path of the project folder to automatic routing, 

see [this link for more info](https://github.com/zalando/connexion#automatic-routing). The default value is `project`.

### Example

```yaml
pyms:
  services:
    swagger:
      path: "swagger"
      file: "swagger.yaml"
      url: "/ui/"
      project_dir: "project.views"
```

## Requests

Extend the [requests library](http://docs.python-requests.org/en/master/) with trace headers and parsing JSON objects.
Encapsulate common rest operations between business services propagating trace headers if set up.

### Configuration

The parameters you can add to your config are:

* **data:** wrap the response in a data field of an envelope object, and add other meta data to that wrapper. The default value is None
* **retries:** If the response is not correct, send again the request. The default number of retries is 3.
* **status_retries:** List of response status code that consider "not correct". The default values are [500, 502, 504]
* **propagate_headers:** Propagate the headers of the actual execution to the request. The default values is False

### Example

```yaml
pyms:
  services:
    requests:
      data: "data"
      retries: 4
      status_retries: [400, 401, 402, 403, 404, 405, 500, 501, 502, 503]
      propagate_headers: true
```

## Tracer

Add trace to all executions with [opentracing](https://github.com/opentracing-contrib/python-flask).

### Configuration

The parameters you can add to your config are:

* **client:** set the client to use traces, The actual options are [Jaeger](https://github.com/jaegertracing/jaeger-client-python) and [Lightstep](https://github.com/lightstep/lightstep-tracer-python). The default value is jaeger.
* **host:** The url to send the data of traces. Check [this tutorial](https://opentracing.io/guides/python/quickstart/) to create your own server
* **component_name:** The name of your application to show in Prometheus metrics

### Example

```yaml
pyms:
  services:
    tracer:
      client: "jaeger"
      host: "localhost"
      component_name: "Python Microservice"
```

## Metrics
Adds [Prometheus](https://prometheus.io/) metrics using the [Prometheus Client
Library](https://github.com/prometheus/client_python).

At the moment, the next metrics are available:

- Incoming requests latency as a histogram
- Incoming requests number as a counter, divided by HTTP method, endpoint and
  HTTP status
- Total number of log events divided by level
- If `tracer` service activated and it's jaeger, it will show its metrics

### Example

```yaml
pyms:
  services:
		metrics: true
```

This will add the endpoint `/metrics` to your microservice, which will expose
the metrics.

## How to contrib: create your own service

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

* Your service will be setted inside `ms` object in `flask.current_app` objetct. for example, with the last config,
you can print the next code:

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

This output in `http://localhost:5000/`:

```json
{"myvalue": 5, "myvalue2": 1}
```