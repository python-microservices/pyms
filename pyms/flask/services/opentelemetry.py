import logging
import time
from typing import Text

from flask import Blueprint, Response, request
from pyms.flask.services.driver import DriverService

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics import Counter, MeterProvider, ValueRecorder
from opentelemetry.sdk.metrics.export.controller import PushController
from prometheus_client import generate_latest

# TODO set sane defaults
# https://github.com/python-microservices/pyms/issues/218
# TODO validate config
# https://github.com/python-microservices/pyms/issues/219
PROMETHEUS_CLIENT = "prometheus"


class FlaskMetricsWrapper:
    def __init__(self, app_name: str, meter: MeterProvider):
        self.app_name = app_name
        # TODO add Histogram support for flask when available
        # https://github.com/open-telemetry/opentelemetry-python/issues/1255
        self.flask_request_latency = meter.create_metric(
            "http_server_requests_seconds",
            "Flask Request Latency",
            "http_server_requests_seconds",
            float,
            ValueRecorder,
            ("service", "method", "uri", "status"),
        )
        self.flask_request_count = meter.create_metric(
            "http_server_requests_count",
            "Flask Request Count",
            "http_server_requests_count",
            int,
            Counter,
            ["service", "method", "uri", "status"],
        )

    def before_request(self):  # pylint: disable=R0201
        request.start_time = time.time()

    def after_request(self, response: Response) -> Response:
        if hasattr(request.url_rule, "rule"):
            path = request.url_rule.rule
        else:
            path = request.path
        request_latency = time.time() - request.start_time
        labels = {
            "service": self.app_name,
            "method": str(request.method),
            "uri": path,
            "status": str(response.status_code),
        }

        self.flask_request_latency.record(request_latency, labels)
        self.flask_request_count.add(1, labels)

        return response


class Service(DriverService):
    """
    Adds [OpenTelemetry](https://opentelemetry.io/) metrics using the [Opentelemetry Client Library](https://opentelemetry-python.readthedocs.io/en/latest/exporter/).
    """

    config_resource: Text = "opentelemetry"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blueprint = Blueprint("opentelemetry", __name__)
        self.serve_metrics()

    def set_metrics_backend(self):
        # Set meter provider
        metrics.set_meter_provider(MeterProvider())
        self.meter = metrics.get_meter(__name__)
        if self.config.metrics.backend.lower() == PROMETHEUS_CLIENT:
            exporter = PrometheusMetricsExporter()
        else:
            pass
        # Create the push controller that will update the metrics when the
        # interval is met
        PushController(self.meter, exporter, self.config.metrics.interval)

    def set_tracing_backend(self):
        pass

    def set_logging_backend(self):
        pass

    def monitor(self, app_name, app):
        metric = FlaskMetricsWrapper(app_name, self.meter)
        app.before_request(metric.before_request)
        app.after_request(metric.after_request)

    def serve_metrics(self):
        @self.blueprint.route("/metrics", methods=["GET"])
        def metrics():  # pylint: disable=unused-variable
            return Response(
                generate_latest(),
                mimetype="text/print()lain",
                content_type="text/plain; charset=utf-8",
            )

    def add_logger_handler(
        self, logger: logging.Logger, service_name: str
    ) -> logging.Logger:
        logger.addHandler(MetricsLogHandler(service_name, self.meter))
        return logger


class MetricsLogHandler(logging.Handler):
    """A LogHandler that exports logging metrics for OpenTelemetry."""

    def __init__(self, app_name: str, meter: MeterProvider):
        super().__init__()
        self.app_name = str(app_name)
        self.logger_total_messages = meter.create_metric(
            "logger_messages_total",
            "Count of log entries by service and level.",
            "logger_messages_total",
            int,
            Counter,
            ["service", "level"],
        )

    def emit(self, record) -> None:
        labels = {"service": self.app_name, "level": record.levelname}
        self.logger_total_messages.add(1, labels)
