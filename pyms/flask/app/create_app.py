import logging
import os
from typing import Text

import connexion
from flask import Flask
from flask_opentracing import FlaskTracing

from pyms.config import get_conf
from pyms.constants import LOGGER_NAME, SERVICE_ENVIRONMENT
from pyms.flask.healthcheck import healthcheck_blueprint
from pyms.flask.services.driver import ServicesManager
from pyms.logger import CustomJsonFormatter
from pyms.utils import check_package_exists

logger = logging.getLogger(LOGGER_NAME)


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """
    _instances = {}
    _singleton = True

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances or not cls._singleton:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]


class Microservice(metaclass=SingletonMeta):
    service = None
    application = None
    swagger = False
    request = False
    tracer = False
    _singleton = True

    def __init__(self, *args, **kwargs):
        self.service = kwargs.get("service", os.environ.get(SERVICE_ENVIRONMENT, "ms"))
        self.path = os.path.dirname(kwargs.get("path", __file__))
        self.config = get_conf(service=self.service, memoize=self._singleton)
        self.init_services()

    def init_services(self):
        service_manager = ServicesManager()
        for service_name, service in service_manager.get_services():
            setattr(self, service_name, service)

    def init_libs(self):
        return self.application

    def init_tracer(self):
        if self._exists_service("tracer"):
            client = self.tracer.get_client()
            self.application.tracer = FlaskTracing(client, True, self.application)

    def init_logger(self):
        self.application.logger = logger
        os.environ['WERKZEUG_RUN_MAIN'] = "true"

        formatter = CustomJsonFormatter('(timestamp) (level) (name) (module) (funcName) (lineno) (message)')
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
        if self._exists_service("swagger"):
            check_package_exists("connexion")
            app = connexion.App(__name__, specification_dir=os.path.join(self.path, self.swagger.path))
            app.add_api(
                self.swagger.file,
                arguments={'title': self.config.APP_NAME},
                base_path=self.config.APPLICATION_ROOT
            )

            # Invert the objects, instead connexion with a Flask object, a Flask object with
            application = app.app
            application.connexion_app = app
        else:
            check_package_exists("flask")
            application = Flask(__name__, static_folder=os.path.join(self.path, 'static'),
                                template_folder=os.path.join(self.path, 'templates'))

        application.root_path = self.path

        return application

    def init_metrics(self):
        if getattr(self, "metrics", False) and self.metrics:
            self.application.register_blueprint(self.metrics.metrics_blueprint)
            self.metrics.add_logger_handler(
                self.application.logger,
                self.application.config["APP_NAME"]
            )
            self.metrics.monitor(self.application)

    def create_app(self):
        """Initialize the Flask app, register blueprints and initialize
        all libraries like Swagger, database,
        the trace system...
        return the app and the database objects.
        :return:
        """
        self.application = self.init_app()
        self.application.config.from_object(self.config)
        self.application.tracer = None
        self.application.ms = self

        # Initialize Blueprints
        self.application.register_blueprint(healthcheck_blueprint)

        self.init_libs()
        self.add_error_handlers()

        self.init_tracer()

        self.init_logger()

        self.init_metrics()

        return self.application

    def _exists_service(self, service_name: Text) -> bool:
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
