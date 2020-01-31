import os
import unittest.mock

from prometheus_client import generate_latest

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from tests.common import MyMicroservice


class TestMetricsFlask(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-metrics.yml")
        ms = MyMicroservice(path=__file__)
        ms.reload_conf()
        self.app = ms.create_app()
        self.client = self.app.test_client()

    def test_metrics_latency(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_latency_root = b'flask_request_latency_seconds_bucket{endpoint="/",le="0.005",method="GET"}'
        generated_latency_metrics = b'flask_request_latency_seconds_bucket{endpoint="/metrics",le="0.005",method="GET"}'
        assert generated_latency_root in generate_latest()
        assert generated_latency_metrics in generate_latest()

    def test_metrics_count(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_count_root = b'flask_request_count_total{endpoint="/",http_status="404",method="GET"}'
        generated_count_metrics = b'flask_request_count_total{endpoint="/metrics",http_status="200",method="GET"}'
        assert generated_count_root in generate_latest()
        assert generated_count_metrics in generate_latest()

    def test_metrics_logger(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_logger = b'python_logging_messages_total{level="DEBUG",service="Python Microservice with Jaeger"}'
        assert generated_logger in generate_latest()

    def test_metrics_jaeger(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_logger = b'jaeger:reporter_spans_total'
        assert generated_logger in generate_latest()
