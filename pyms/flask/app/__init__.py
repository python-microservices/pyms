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

    def __init__(self, service: Text, path=__file__):
        self.service = service
        self.path = os.path.dirname(path)

    def init_libs(self, app):
        return app

    def create_app(self):
        """Initialize the Flask app, register blueprints and initialize
        all libraries like Swagger, database,
        the trace system...
        return the app and the database objects.
        :return: application
        """
        config = get_conf(service=self.service)
        app = connexion.App(__name__, specification_dir=os.path.join(self.path, 'swagger'))
        app.add_api('swagger.yaml',
                    arguments={'title': 'Swagger Example project'},
                    base_path=config.APPLICATION_ROOT
                    )

        application = app.app
        application.config.from_object(get_conf(service=self.service))
        application.tracer = None

        # Initialize Blueprints
        application.register_blueprint(healthcheck_blueprint)
        self.init_libs(application)
        # Inject Modules
        formatter = CustomJsonFormatter('(timestamp) (level) (name) (module) (funcName) (lineno) (message) (traceback)')

        if not application.config["TESTING"]:

            log_handler = logging.StreamHandler()

            application.tracer = FlaskTracer(init_jaeger_tracer(), True, application)
            formatter.add_service_name(application.config["APP_NAME"])
            formatter.add_trace_span(application.tracer)
            log_handler.setFormatter(formatter)
            application.logger.addHandler(log_handler)
            application.logger.setLevel(logging.INFO)

        return application
