import logging
import os

import connexion
from flask import Flask
from flask_opentracing import FlaskTracing

from pyms.config.conf import get_conf
from pyms.constants import LOGGER_NAME, SERVICE_ENVIRONMENT
from pyms.flask.healthcheck import healthcheck_blueprint
from pyms.flask.services.driver import ServicesManager, DriverService
from pyms.logger import CustomJsonFormatter
from pyms.tracer.main import init_lightstep_tracer

logger = logging.getLogger(LOGGER_NAME)


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]


class Microservice(metaclass=SingletonMeta):
    service = None
    application = None
    swagger = DriverService
    requests = DriverService

    def __init__(self, *args, **kwargs):
        self.service = kwargs.get("service", os.environ.get(SERVICE_ENVIRONMENT, "ms"))
        self.path = os.path.dirname(kwargs.get("path", __file__))
        self.config = get_conf(service=self.service)
        self.init_services()

    def init_services(self):
        service_manager = ServicesManager()
        for service_name, service in service_manager.get_services():
            setattr(self, service_name, service)

    def init_libs(self):
        return self.application

    def init_tracer(self):
        self.application.opentracing_tracer = init_lightstep_tracer(self.application.config["APP_NAME"])
        self.application.tracer = FlaskTracing(self.application.opentracing_tracer, True, self.application)

    def init_logger(self):
        self.application.logger = logger
        os.environ['WERKZEUG_RUN_MAIN'] = "true"

        formatter = CustomJsonFormatter('(timestamp) (level) (name) (module) (funcName) (lineno) (message)')
        formatter.add_service_name(self.application.config["APP_NAME"])
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)

        self.application.logger.addHandler(log_handler)
        self.application.logger.propagate = False
        self.application.logger.setLevel(logging.INFO)

    def init_app(self) -> Flask:
        if getattr(self, "swagger", False):
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
            application = Flask(__name__, static_folder=os.path.join(self.path, 'static'),
                                template_folder=os.path.join(self.path, 'templates'))

        application.root_path = self.path

        return application

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

        # Initialize Blueprints
        self.application.register_blueprint(healthcheck_blueprint)

        self.init_libs()
        self.add_error_handlers()

        self.init_tracer()

        self.init_logger()

        return self.application

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
