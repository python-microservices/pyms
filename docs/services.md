# Services

Services are libraries, resources and extensions added to the Microservice in the configuration file.
These services are created as an attribute of the [Microservice class](ms_class.md) to use in the code.

To add a service check the [configuration section](configuration.md).

You can declare a service but activate/deactivate with the keyword `enabled`, like so:

```yaml
pyms:
  services:
    requests:
      enabled: false
```

Currently availabe services are:

## Swagger / connexion

Extends the Microservice with [Connexion](https://github.com/zalando/connexion) and [swagger-ui](https://github.com/sveint/flask-swagger-ui).

### Installation

You must install `pyms` with `pip install py-ms[all]` or `pip install py-ms[swagger]`

### Configuration

The parameters you can add to your config are the folowing:

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
Encapsulates common rest operations between business services propagating trace headers if set up.

### Installation

You must install `pyms` with `pip install py-ms[all]` or `pip install py-ms[request]`

### Configuration

The parameters you can add to your config are:

* **data:** wrap the response in a data field of an envelope object, and add other meta data to that wrapper. The default value is None
* **retries:** If the response is not correct, this specifies the amount of times it performs the request again. The default number of retries is 3.
* **status_retries:** List of response status codes that are considered "not correct". The default values are [500, 502, 504]
* **propagate_headers:** Propagate the headers of the current execution to the request. The default values is False

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

Add traces to all executions with [opentracing](https://github.com/opentracing-contrib/python-flask). This service
solves the problem of [distributed tracing](https://microservices.io/patterns/observability/distributed-tracing.html)

### Installation

You must install `pyms` with `pip install pyms[all]` or `pip install pyms[trace]`

### Configuration

The parameters you can add to your config are:

* **client:** set the client that will receive the traces, The current options are [Jaeger](https://github.com/jaegertracing/jaeger-client-python) and [Lightstep](https://github.com/lightstep/lightstep-tracer-python). The default value is jaeger.
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

The folowing metrics are currently available:

- Incoming requests latency as a histogram
- Incoming requests number as a counter, divided by HTTP method, endpoint and
  HTTP status
- Total number of log events divided by level
- If `tracer` service activated and it's jaeger, it will show its metrics

### Installation

You must install `pyms` with `pip install py-ms[all]` or `pip install py-ms[metrics]`

### Example

```yaml
pyms:
  services:
		metrics: true
```

This will add the endpoint `/metrics` to your microservice, which will expose
the metrics.

## How to contrib: 

[See tutorial](tutorial_create_services.md)