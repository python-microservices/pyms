import logging

import prometheus_client

# Based on https://github.com/korfuri/python-logging-prometheus/

log_entries = prometheus_client.Counter(
    "python_logging_messages_total",
    "Count of log entries by service and level.",
    ["service", "level"],
)


def logger_metrics(app_name, logger):
    class ExportingLogHandler(logging.Handler):
        """A LogHandler that exports logging metrics for Prometheus.io."""

        def emit(self, record):
            log_entries.labels(app_name, record.levelname).inc()

    logger.addHandler(ExportingLogHandler())
    return logger
