# Services

Services are libraries, resources and extensions added to the Microservice in the configuration file.
This services are created as an attribute of the [Microservice class](ms_class.md) to use in the code.

To add a service check the [configuration section](configuration.md).

Current services are:

## Swagger / connexion
Extends the Microservice with [Connexion](https://github.com/zalando/connexion)

## Requests
Extend the [requests library](http://docs.python-requests.org/en/master/) with trace headers and parsing JSON objects.
Encapsulate common rest operations between business services propagating trace headers if set up.

## Metrics
Adds [Prometheus](https://prometheus.io/) metrics using the [Prometheus Client
Library](https://github.com/prometheus/client_python).

At the moment, the next metrics are available:
- Incoming requests latency as a histogram
- Incoming requests number as a counter, divided by HTTP method, endpoint and
  HTTP status
- Total number of log events divided by level
- If `tracer` service activated and it's jaeger, it will show its metrics

To use this service, you may add the next to you configuration file:

```yaml
pyms:
  metrics: true
```

This will add the endpoint `/metrics` to your microservice, which will expose
the metrics.

## How to contrib: create your own service:

TODO
