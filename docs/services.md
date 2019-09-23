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


## How to contrib: create your own service:

TODO