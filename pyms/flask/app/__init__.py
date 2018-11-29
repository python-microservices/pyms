import logging
import os
from typing import Text

import connexion
from flask_opentracing import FlaskTracer

from pyms.config.conf import get_conf
from pyms.flask.healthcheck import healthcheck_blueprint
from pyms.logger import CustomJsonFormatter
from pyms.tracer.main import init_jaeger_tracer


class Microservice:
    service = None
    application = None

    def __init__(self, service: Text, path=__file__):
        self.service = service
        self.path = os.path.dirname(path)

    def init_libs(self):
        return self.application

    def create_app(self):
        """Initialize the Flask app, register blueprints and initialize
        all libraries like Swagger, database,
        the trace system...
        return the app and the database objects.
        :return:
        """
        config = get_conf(service=self.service)
        app = connexion.App(__name__, specification_dir=os.path.join(self.path, 'swagger'))
        app.add_api('swagger.yaml',
                    arguments={'title': 'Swagger Example project'},
                    base_path=config.APPLICATION_ROOT
                    )

        self.application = app.app
        self.application._connexion_app = app
        self.application.config.from_object(get_conf(service=self.service))
        self.application.tracer = None

        # Initialize Blueprints
        self.application.register_blueprint(healthcheck_blueprint)

        self.init_libs()
        self.add_error_handlers()

        # Inject Modules
        formatter = CustomJsonFormatter('(timestamp) (level) (name) (module) (funcName) (lineno) (message)')
        if not self.application.config["TESTING"]:
            log_handler = logging.StreamHandler()

            self.application.tracer = FlaskTracer(init_jaeger_tracer(), True, self.application)
            formatter.add_service_name(self.application.config["APP_NAME"])
            formatter.add_trace_span(self.application.tracer)
            log_handler.setFormatter(formatter)
            self.application.logger.addHandler(log_handler)
            self.application.logger.setLevel(logging.INFO)

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

        self.application._connexion_app.add_error_handler(code_or_exception, handler)
