# Welcome to PyMS

PyMS, Python MicroService, is a [Microservice chassis pattern](https://microservices.io/patterns/microservice-chassis.html) 
like Spring Boot (Java) or Gizmo (Golang). PyMS is a collection of libraries, best practices and recommended ways to build 
microservices with Python which handles cross-cutting concerns: 

- Externalized configuration
- Logging
- Health checks
- Metrics
- Distributed tracing

PyMS is powered by [Flask](https://flask.palletsprojects.com/en/1.1.x/), [Connexion](https://github.com/zalando/connexion) 
and [Opentracing](https://opentracing.io/).

Get started with [Installation](installation.md) and then get an overview with the [Quickstart](quickstart.md). 

## Motivation

When we started to create microservice with no idea, we were looking for tutorials, guides, best practices, but we found
nothing to create professional projects. Most articles say:

- "Install flask"
- "Create routes"
- (Sometimes) "Create a swagger specs"
- "TA-DA! you have a microservice"

But... what happens with our configuration out of code like Kubernetes configmap? what happens with transactionality? 
If we have many microservices, what happens with traces?.

There are many problems around Python and microservices and we can`t find anyone to give a solution.

We start creating these projects to try to solve all the problems we have found in our professional lives about 
microservices architecture.

Nowadays, is not perfect and we have a looong roadmap, but we hope this library could help other felas and friends ;) 


## Index
* [Installation](installation.md)
* [Quickstart](quickstart.md)
* [Configuration](configuration.md)
* [Encrypt/Decrypt Configuration](encrypt_decryt_configuration.md)
* [Services](services.md)
* [PyMS structure](structure.md)
* [Microservice class](ms_class.md)
* [Examples](examples.md)
* [Routing](routing.md)
* [Structure of a microservice project](structure_project.md)
