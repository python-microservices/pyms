# Structure

### pyms/config
Module to read yaml or json configuration from a dictionary or a path.

### pyms/flask/app
With the function `create_app` initialize the Flask app, register [blueprints](http://flask.pocoo.org/docs/0.12/blueprints/)
and initialize all libraries such as Swagger, database, trace system, custom logger format, etc.

### pyms/flask/services
Integrations and wrappers over common libs like request, swagger, connexion or metrics.

### pyms/flask/healthcheck
This view is usually used by Kubernetes, Eureka and other systems to check if our application is running.

### pyms/logger
Print logger in JSON format to send to server like Elasticsearch. Inject span traces in logger.

### pyms/tracer
Create an injector `flask_opentracing.FlaskTracer` to use in our projects.
