import time
import logging

from flask import Blueprint, Response, request
from prometheus_client import Counter, Histogram, generate_latest
from pyms.flask.services.driver import DriverService

# Based on https://github.com/sbarratt/flask-prometheus
# and https://github.com/korfuri/python-logging-prometheus/

FLASK_REQUEST_LATENCY = Histogram(
    "flask_request_latency_seconds", "Flask Request Latency", ["method", "endpoint"]
)
FLASK_REQUEST_COUNT = Counter(
    "flask_request_count", "Flask Request Count", ["method", "endpoint", "http_status"]
)

LOGGER_TOTAL_MESSAGES = Counter(
    "python_logging_messages_total",
    "Count of log entries by service and level.",
    ["service", "level"],
)


def before_request():
    request.start_time = time.time()


def after_request(response):
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()

    return response


class Service(DriverService):
    service = "metrics"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics_blueprint = Blueprint("metrics", __name__)
        self.serve_metrics()

    @staticmethod
    def monitor(app):
        app.before_request(before_request)
        app.after_request(after_request)

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
