import logging

import prometheus_client

# Based on https://github.com/korfuri/python-logging-prometheus/

log_entries = prometheus_client.Counter(
    "python_logging_messages_total",
    "Count of log entries by service and level.",
    ["service", "level"],
)


class ExportingLogHandler(logging.Handler):
    """A LogHandler that exports logging metrics for Prometheus.io."""

    # def __init__(self, app_name, *args, **kwargs):
    def __init__(self, app_name):
        super(ExportingLogHandler, self).__init__()
        self.app_name = app_name

    def emit(self, record):
        log_entries.labels(self.app_name, record.levelname).inc()


def logger_metrics(app_name, logger):

    logger.addHandler(ExportingLogHandler(app_name))
    return logger
