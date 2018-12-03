# Structure

### pyms/config
Module to read yaml or json configuration from a dictionary or a path.

### pyms/flask/app
With the funcion `create_app` initialize the Flask app, register [blueprints](http://flask.pocoo.org/docs/0.12/blueprints/)
and intialize all libraries like Swagger, database, trace system, custom logger format, etc.

### pyms/flask/healthcheck
This views is usually used by Kubernetes, Eureka and other systems to check if our application is up and running.

### pyms/logger
Print logger in JSON format to send to server like Elasticsearch. Inject span traces in logger.

### pyms/rest_template
Encapsulate common rest operations between business services propagating trace headers if configured.

### pyms/tracer
Create an injector `flask_opentracing.FlaskTracer` to use in our projects