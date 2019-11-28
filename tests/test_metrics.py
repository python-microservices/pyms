#!/usr/bin/env python

import unittest.mock
from flask import Flask
from pyms.flask.metrics import metrics_blueprint, monitor
from prometheus_client import generate_latest


class TestMetricsFlask(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(metrics_blueprint)
        self.client = self.app.test_client()

    def test_metrics_latency(self):
        monitor(self.app)
        generated_latency = b'flask_request_latency_seconds_bucket{endpoint="/",le="0.005",method="GET"}'
        assert generated_latency in generate_latest()

    def test_metrics_count(self):
        monitor(self.app)
        generated_count = (
            b'flask_request_count_total{endpoint="/",http_status="404",method="GET"}'
        )
        assert generated_count in generate_latest()
