import logging
import time

from flask import Blueprint, Flask, Response, request
from prometheus_client import REGISTRY, CollectorRegistry, Counter, Histogram, generate_latest, multiprocess

from pyms.flask.services.driver import DriverService

# Based on https://github.com/sbarratt/flask-prometheus
# and https://github.com/korfuri/python-logging-prometheus/

FLASK_REQUEST_LATENCY = Histogram(
    "http_server_requests_seconds", "Flask Request Latency", ["service", "method", "uri", "status"]
)
FLASK_REQUEST_COUNT = Counter(
    "http_server_requests_count", "Flask Request Count", ["service", "method", "uri", "status"]
)

LOGGER_TOTAL_MESSAGES = Counter(
    "logger_messages_total",
    "Count of log entries by service and level.",
    ["service", "level"],
)


class FlaskMetricsWrapper:
    def __init__(self, app_name):
        self.app_name = app_name

    def before_request(self) -> None:  # pylint: disable=R0201
        request.start_time = time.time()

    def after_request(self, response: Response) -> Response:
        if hasattr(request.url_rule, "rule"):
            path = request.url_rule.rule
        else:
            path = request.path
        request_latency = time.time() - request.start_time
        FLASK_REQUEST_LATENCY.labels(self.app_name, request.method, path, response.status_code).observe(request_latency)
        FLASK_REQUEST_COUNT.labels(self.app_name, request.method, path, response.status_code).inc()

        return response


class Service(DriverService):
    """
    Adds [Prometheus](https://prometheus.io/) metrics using the [Prometheus Client Library](https://github.com/prometheus/client_python).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics_blueprint = Blueprint("metrics", __name__)
        self.init_registry()
        self.serve_metrics()

    def init_action(self, microservice_instance):
        microservice_instance.application.register_blueprint(microservice_instance.metrics.metrics_blueprint)
        self.add_logger_handler(
            microservice_instance.application.logger, microservice_instance.application.config["APP_NAME"]
        )
        self.monitor(microservice_instance.application.config["APP_NAME"], microservice_instance.application)

    def init_registry(self) -> None:
        try:
            multiprocess_registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(multiprocess_registry)
            self.registry = multiprocess_registry
        except ValueError:
            self.registry = REGISTRY

    @staticmethod
    def monitor(app_name: str, app: Flask) -> None:
        metric = FlaskMetricsWrapper(app_name)
        app.before_request(metric.before_request)
        app.after_request(metric.after_request)

    def serve_metrics(self):
        @self.metrics_blueprint.route("/metrics", methods=["GET"])
        def metrics():  # pylint: disable=unused-variable
            return Response(
                generate_latest(self.registry),
                mimetype="text/print()lain",
                content_type="text/plain; charset=utf-8",
            )

    @staticmethod
    def add_logger_handler(logger: logging.Logger, service_name: str) -> logging.Logger:
        logger.addHandler(MetricsLogHandler(service_name))
        return logger


class MetricsLogHandler(logging.Handler):
    """A LogHandler that exports logging metrics for Prometheus.io."""

    def __init__(self, app_name):
        super().__init__()
        self.app_name = app_name

    def emit(self, record) -> None:
        LOGGER_TOTAL_MESSAGES.labels(self.app_name, record.levelname).inc()
