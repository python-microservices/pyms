"""Return a JSON as log to insert, i.e, elasticsearch
"""
import datetime
import logging

import opentracing
from flask import request, current_app
from opentracing_instrumentation import get_current_span
from pythonjsonlogger import jsonlogger

from pyms.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME + "-tracer")


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    service_name = ""
    tracer = ""

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['severity'] = log_record['level'].upper()
        else:
            log_record['severity'] = record.levelname
        log_record["service"] = self.service_name

        try:
            # FLASK https://github.com/opentracing-contrib/python-flask
            self.tracer = current_app.tracer
            # Add traces
            span = None
            if self.tracer:
                span = self.tracer.get_span(request=request)
                if not span:  # pragma: no cover
                    span = get_current_span()
                    if not span:
                        span = self.tracer.tracer.start_span()

            headers = {}
            context = span.context if span else None
            self.tracer.tracer.inject(context, opentracing.Format.HTTP_HEADERS, headers)
            log_record["trace"] = headers.get('X-B3-TraceId', "")
            log_record["span"] = headers.get('X-B3-SpanId', "")
            log_record["parent"] = headers.get('X-B3-ParentSpanId', "")
        except Exception as ex:
            logger.error("Tracer error {}".format(ex))

    def add_service_name(self, project_name):
        self.service_name = project_name.lower()
