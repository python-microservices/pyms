import os
import unittest.mock

from prometheus_client import generate_latest

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from tests.common import MyMicroserviceNoSingleton


class TestMetricsFlask(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-metrics.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        ms.reload_conf()
        self.app = ms.create_app()
        self.client = self.app.test_client()

    def test_metrics_latency(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_latency_root = b'http_server_requests_seconds_bucket{le="0.005",method="GET",service="Python Microservice",status="200",uri="/"}'
        generated_latency_metrics = b'http_server_requests_seconds_bucket{le="0.005",method="GET",service="Python Microservice with Jaeger",status="200",uri="/metrics"}'
        assert generated_latency_root in generate_latest()
        assert generated_latency_metrics in generate_latest()

    def test_metrics_count(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_count_root = b'http_server_requests_count_total{method="GET",service="Python Microservice",status="200",uri="/"}'
        generated_count_metrics = b'http_server_requests_count_total{method="GET",service="Python Microservice with Jaeger",status="200",uri="/metrics"}'
        assert generated_count_root in generate_latest()
        assert generated_count_metrics in generate_latest()

    def test_metrics_logger(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_logger = b'logger_messages_total{level="DEBUG",service="Python Microservice with Jaeger"}'
        assert generated_logger in generate_latest()

    def test_metrics_jaeger(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_logger = b'jaeger:reporter_spans_total'
        assert generated_logger in generate_latest()
