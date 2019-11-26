from __future__ import unicode_literals, print_function, absolute_import, division

import time

from flask import Blueprint, Response, request
from prometheus_client import Counter, Histogram, generate_latest

# Based on https://github.com/sbarratt/flask-prometheus

metrics_blueprint = Blueprint("metrics", __name__)

FLASK_REQUEST_LATENCY = Histogram(
    "flask_request_latency_seconds", "Flask Request Latency", ["method", "endpoint"]
)
FLASK_REQUEST_COUNT = Counter(
    "flask_request_count", "Flask Request Count", ["method", "endpoint", "http_status"]
)


def before_request():
    request.start_time = time.time()


def after_request(response):
    request_latency = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
    FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()

    return response


def monitor(app):
    app.before_request(before_request)
    app.after_request(after_request)


@metrics_blueprint.route("/metrics", methods=["GET"])
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain",
        content_type="text/plain; charset=utf-8",
    )
