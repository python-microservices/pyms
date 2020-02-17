# Routing
With PyMS you can extend the Microservice with [Connexion](https://github.com/zalando/connexion) and [swagger-ui](https://github.com/sveint/flask-swagger-ui).

To use connexion, you must set in your config.yaml this:
```yaml
pyms:
  services:
    [...]
    swagger:
      path: ""
      file: "swagger.yaml"
  config:
    [...]
```

If you want to know more about configure swagger service, see [Service section](services.md).

Now, you can create a `swagger.yaml` file with [OpenAPI Specification](https://swagger.io/specification/). 

# Examples of routing

You can see how structure a project or OpenAPI Specification in 
[PyMS examples](https://github.com/python-microservices/pyms/tree/master/examples/microservice_swagger) or in 
[Microservice Scaffold](https://github.com/python-microservices/microservices-scaffold)

## Routing to files

This section is equal from [Zalando Connexion](https://github.com/zalando/connexion#automatic-routing), because PyMS use
this library to route endpoints to functions:

**Explicit Routing**:

```yaml
paths:
  /hello_world:
    post:
      operationId: myapp.api.hello_world
```

If you provide this path in your specification POST requests to
``http://MYHOST/hello_world``, it will be handled by the function
``hello_world`` in the ``myapp.api`` module. Optionally, you can include
``x-swagger-router-controller`` (or ``x-openapi-router-controller``) in your
operation definition, making ``operationId`` relative:

```yaml
paths:
  /hello_world:
    post:
      x-swagger-router-controller: myapp.api
      operationId: hello_world
```

Keep in mind that Connexion follows how `HTTP methods work in Flask`_ and therefore HEAD requests will be handled by the ``operationId`` specified under GET in the specification. If both methods are supported, ``connexion.request.method`` can be used to determine which request was made.

## Automatic Routing

To customize this behavior, Connexion can use alternative
``Resolvers``--for example, ``RestyResolver``. The ``RestyResolver``
will compose an ``operationId`` based on the path and HTTP method of
the endpoints in your specification:

```python
from pyms.flask.app import Microservice

ms = Microservice(path=__file__)
```

```yaml
paths:
  /:
    get:
      # Implied operationId: api.get
  /foo:
    get:
      # Implied operationId: api.foo.search
    post:
      # Implied operationId: api.foo.post
  '/foo/{id}':
    get:
      # Implied operationId: api.foo.get
    put:
      # Implied operationId: api.foo.put
    copy:
      # Implied operationId: api.foo.copy
    delete:
      # Implied operationId: api.foo.delete
```

``RestyResolver`` will give precedence to any ``operationId`` encountered in the specification. It will also respect
``x-router-controller``. You can import and extend ``connexion.resolver.Resolver`` to implement your own ``operationId``
(and function) resolution algorithm.

Automatic Parameter Handling
----------------------------

Connexion automatically maps the parameters defined in your endpoint specification to arguments of your Python views as named parameters, and, whenever possible, with value casting. Simply define the endpoint's parameters with the same names as your views arguments.

As an example, say you have an endpoint specified as:

```yaml
paths:
	/foo:
		get:
			operationId: api.foo_get
			parameters:
				- name: message
					description: Some message.
					in: query
					type: string
					required: true
```

And the view function:

```python
# api.py file

def foo_get(message):
		# do something
		return 'You send the message: {}'.format(message), 200
```

In this example, Connexion automatically recognizes that your view
function expects an argument named ``message`` and assigns the value
of the endpoint parameter ``message`` to your view function.