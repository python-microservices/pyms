"""Return a JSON as log to insert, i.e, elasticsearch
"""
import datetime
import logging

import opentracing
from flask import request, current_app
from pythonjsonlogger import jsonlogger

from pyms.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


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
            span = self.tracer.get_span(request=request)
            headers = {}
            self.tracer.tracer.inject(span.context, opentracing.Format.HTTP_HEADERS, headers)
            log_record["trace"] = headers['ot-tracer-traceid']
            log_record["span"] = headers['ot-tracer-spanid']
            log_record["parent"] = headers.get('ot-tracer-parentspanid', '')
        except Exception as ex:
            logger.debug("Tracer error {}".format(ex))

    def add_service_name(self, project_name):
        self.service_name = project_name.lower()
