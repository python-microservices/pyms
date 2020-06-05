import logging
import os
from typing import Text

from flask import Flask

from pyms.config.conf import validate_conf
from pyms.config.resource import ConfigResource
from pyms.constants import LOGGER_NAME, CONFIG_BASE
from pyms.crypt.driver import CryptResource
from pyms.flask.app.utils import SingletonMeta, ReverseProxied
from pyms.flask.healthcheck import healthcheck_blueprint
from pyms.flask.services.driver import ServicesResource
from pyms.logger import CustomJsonFormatter
from pyms.utils import check_package_exists, import_from

logger = logging.getLogger(LOGGER_NAME)


class Microservice(ConfigResource, metaclass=SingletonMeta):
    """The class Microservice is the core of all microservices built with PyMS.
    You can create a simple microservice such as:
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
    Environments variables of PyMS:
    **CONFIGMAP_FILE**: The path to the configuration file. By default, PyMS search the configuration file in your
    actual folder with the name "config.yml"

    ## Create configuration
    Each microservice needs a config file in yaml or json format to work with it. This configuration contains
    the Flask settings of your project and the [Services](services.md). With this way to create configuration files, we
    solve two problems of the [12 Factor apps](https://12factor.net/):
    - Store config out of the code
    - Dev/prod parity: the configuration could be injected and not depends of our code, for example, Kubernetes config maps

    a simple configuration file could be a config.yaml:

    ```yaml
    pyms:
      services:
        requests: true
        swagger:
          path: ""
          file: "swagger.yaml"
      config:
        DEBUG: true
        TESTING: false
        APP_NAME: "Python Microservice"
        APPLICATION_ROOT: ""
    ```

    Services are libraries, resources and extensions added to the Microservice in the configuration file.
    This services are created as an attribute of the [Microservice class](ms_class.md) to use in the code.

    To add a service check the [configuration section](configuration.md).

    Current services are swagger, request, tracer, metrics
    """
    config_resource = CONFIG_BASE
    services = []
    application = None
    swagger = False
    request = False
    tracer = False
    _singleton = True

    def __init__(self, *args, **kwargs):
        """
        You can get the relative path from the current directory with `__file__` in path param. The path must be
        the folder where PyMS search for default config file, default swagger definition and encrypt key.
        :param args:
        :param kwargs: "path", optional, the current directory where `Microservice` class is instanciated
        """
        path = kwargs.pop("path") if kwargs.get("path") else None
        self.path = os.path.abspath("")
        if path:
            self.path = os.path.dirname(os.path.abspath(path))

        validate_conf()
        self.init_crypt(path=self.path, *args, **kwargs)
        super().__init__(path=self.path, crypt=self.crypt, *args, **kwargs)
        self.init_services()

    def init_services(self) -> None:
        """
        Set the Attributes of all service defined in config.yml and exists in `pyms.flask.service` module
        :return: None
        """
        services_resources = ServicesResource()
        for service_name, service in services_resources.get_services():
            if service_name not in self.services or not getattr(self, service_name, False):
                self.services.append(service_name)
                setattr(self, service_name, service)

    def init_crypt(self, *args, **kwargs) -> None:
        """
        Set the Attributes of all service defined in config.yml and exists in `pyms.flask.service` module
        :return: None
        """
        crypt_object = CryptResource(*args, **kwargs)
        self.crypt = crypt_object

    def delete_services(self) -> None:
        """
        Set the Attributes of all service defined in config.yml and exists in `pyms.flask.service` module
        :return: None
        """
        for service_name in self.services:
            try:
                delattr(self, service_name)
            except AttributeError:
                pass

    def init_libs(self) -> Flask:
        """This function exists to override if you need to set more libs such as SQLAlchemy, CORs, and any else
        library needs to be init over flask, like the usual pattern [MYLIB].init_app(app)
        :return:
        """
        return self.application

    def init_tracer(self) -> None:
        """Set attribute in flask `tracer`. See in `pyms.flask.services.tracer` how it works
        :return: None
        """
        if self._exists_service("tracer"):
            FlaskTracing = import_from("flask_opentracing", "FlaskTracing")
            client = self.tracer.get_client()
            self.application.tracer = FlaskTracing(client, True, self.application)

    def init_logger(self) -> None:
        """
        Set a logger and return in JSON format.
        :return:
        """
        self.application.logger = logger
        os.environ['WERKZEUG_RUN_MAIN'] = "true"

        formatter = CustomJsonFormatter()
        formatter.add_service_name(self.application.config["APP_NAME"])
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)

        self.application.logger.addHandler(log_handler)

        self.application.logger.propagate = False

        if self.application.config["DEBUG"]:
            self.application.logger.setLevel(logging.DEBUG)
        else:  # pragma: no cover
            self.application.logger.setLevel(logging.INFO)

    def init_app(self) -> Flask:
        """Set attribute in flask `swagger`. See in `pyms.flask.services.swagger` how it works. If not set,
        run a "normal" Flask app.
        :return: None
        """
        if self._exists_service("swagger"):
            application = self.swagger.init_app(config=self.config.to_flask(), path=self.path)
        else:
            check_package_exists("flask")
            application = Flask(__name__, static_folder=os.path.join(self.path, 'static'),
                                template_folder=os.path.join(self.path, 'templates'))

        application.root_path = self.path

        # Fix connexion issue https://github.com/zalando/connexion/issues/527
        application.wsgi_app = ReverseProxied(application.wsgi_app)

        return application

    def init_metrics(self):
        """Set attribute in flask `metrics`. See in `pyms.flask.services.metrics` how it works
        :return: None
        """
        if getattr(self, "metrics", False) and self.metrics:
            self.application.register_blueprint(self.metrics.metrics_blueprint)
            self.metrics.add_logger_handler(
                self.application.logger,
                self.application.config["APP_NAME"]
            )
            self.metrics.monitor(self.application.config["APP_NAME"], self.application)

    def reload_conf(self):
        self.delete_services()
        self.config.reload()
        self.services = []
        self.init_services()
        self.crypt.config.reload()
        self.create_app()

    def create_app(self):
        """Initialize the Flask app, register blueprints and initialize
        all libraries like Swagger, database,
        the trace system...
        return the app and the database objects.
        :return:
        """
        self.application = self.init_app()
        self.application.config.from_object(self.config.to_flask())
        self.application.tracer = None
        self.application.ms = self

        # Initialize Blueprints
        self.application.register_blueprint(healthcheck_blueprint)

        self.init_libs()
        self.add_error_handlers()

        self.init_tracer()

        self.init_logger()

        self.init_metrics()

        logger.debug("Started app with PyMS and this services: {}".format(self.services))

        return self.application

    def _exists_service(self, service_name: Text) -> bool:
        """Check if service exists in the config.yml file
        :param service_name:
        :return: bool
        """
        service = getattr(self, service_name, False)
        return service and service is not None

    def add_error_handlers(self):
        """Subclasses will override this method in order to add specific error handlers. This should be done with
        calls to add_error_handler method.
        """
        pass

    def add_error_handler(self, code_or_exception, handler):
        """Add custom handler for an error code or exception in the connexion app.

        :param code_or_exception: HTTP error code or exception
        :param handler: callback for error handler
        """
        self.application.connexion_app.add_error_handler(code_or_exception, handler)
