import time
import logging

from flask import Blueprint, Response, request
from prometheus_client import Counter, Histogram, generate_latest
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


class FlaskMetricsWrapper():
    def __init__(self, app_name):
        self.app_name = app_name

    def before_request(self):  # pylint: disable=R0201
        request.start_time = time.time()

    def after_request(self, response):
        request_latency = time.time() - request.start_time
        FLASK_REQUEST_LATENCY.labels(self.app_name, request.method, request.path, response.status_code).observe(request_latency)
        FLASK_REQUEST_COUNT.labels(self.app_name, request.method, request.path, response.status_code).inc()

        return response


class Service(DriverService):
    """
    Adds [Prometheus](https://prometheus.io/) metrics using the [Prometheus Client Library](https://github.com/prometheus/client_python).
    """
    service = "metrics"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics_blueprint = Blueprint("metrics", __name__)
        self.serve_metrics()

    @staticmethod
    def monitor(app_name, app):
        metric = FlaskMetricsWrapper(app_name)
        app.before_request(metric.before_request)
        app.after_request(metric.after_request)

    def serve_metrics(self):
        @self.metrics_blueprint.route("/metrics", methods=["GET"])
        def metrics():  # pylint: disable=unused-variable
            return Response(
                generate_latest(),
                mimetype="text/print()lain",
                content_type="text/plain; charset=utf-8",
            )

    @staticmethod
    def add_logger_handler(logger, service_name):
        logger.addHandler(MetricsLogHandler(service_name))
        return logger


class MetricsLogHandler(logging.Handler):
    """A LogHandler that exports logging metrics for Prometheus.io."""

    def __init__(self, app_name):
        super(MetricsLogHandler, self).__init__()
        self.app_name = app_name

    def emit(self, record):
        LOGGER_TOTAL_MESSAGES.labels(self.app_name, record.levelname).inc()
