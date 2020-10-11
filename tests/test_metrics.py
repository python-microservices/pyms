import os
import unittest.mock
from tempfile import TemporaryDirectory
from pathlib import Path

from prometheus_client import generate_latest
from prometheus_client import values
from opentracing import global_tracer
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.services.metrics import LOGGER_TOTAL_MESSAGES, FLASK_REQUEST_COUNT, FLASK_REQUEST_LATENCY
from tests.common import MyMicroserviceNoSingleton

def reset_metric(metric):
    metric._metric_init() # pylint: disable=protected-access
    metric._metrics = {} # pylint: disable=protected-access

def reset_metrics():
    reset_metric(LOGGER_TOTAL_MESSAGES)
    reset_metric(FLASK_REQUEST_COUNT)
    reset_metric(FLASK_REQUEST_LATENCY)
    try:
        for metric in global_tracer().metrics_factory._cache.values(): # pylint: disable=protected-access
            reset_metric(metric)
    except AttributeError: # Not a  Jaeger tracer
        pass

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
        generated_latency_root = b'http_server_requests_seconds_bucket{le="0.005",method="GET",service="Python Microservice with Jaeger",status="404",uri="/"}'
        generated_latency_metrics = b'http_server_requests_seconds_bucket{le="0.005",method="GET",service="Python Microservice with Jaeger",status="200",uri="/metrics"}'
        assert generated_latency_root in generate_latest()
        assert generated_latency_metrics in generate_latest()

    def test_metrics_count(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_count_root = b'http_server_requests_count_total{method="GET",service="Python Microservice with Jaeger",status="404",uri="/"}'
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

class TestMultiprocessMetricsFlask(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    current = None

    @classmethod
    def current_test(cls):
        return "not_in_test" if cls.current is None else cls.current

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = TemporaryDirectory()
        os.environ["prometheus_multiproc_dir"] = cls.temp_dir.name
        cls.patch_value_class = unittest.mock.patch.object(values, "ValueClass", values.MultiProcessValue(cls.current_test))
        cls.patch_value_class.start()

    def setUp(self):
        TestMultiprocessMetricsFlask.current = self._testMethodName
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-metrics.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        ms.reload_conf()
        reset_metrics()
        self.app = ms.create_app()
        self.client = self.app.test_client()
        for path in Path(self.temp_dir.name).iterdir():
            if self._testMethodName not in path.name:
                path.unlink()

    @classmethod
    def tearDownClass(cls):
        cls.patch_value_class.stop()
        os.environ.pop("prometheus_multiproc_dir")
        reset_metrics()

    def test_metrics_stored_in_directory(self):
        assert TestMultiprocessMetricsFlask.current_test() is not None
        self.client.get("/")
        self.client.get("/metrics")
        metrics = os.listdir(path=self.temp_dir.name)

        assert f"counter_{self._testMethodName}.db" in metrics
        assert f"histogram_{self._testMethodName}.db" in metrics

    def test_metrics_latency(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_latency_root = b'http_server_requests_seconds_bucket{le="0.005",method="GET",service="Python Microservice with Jaeger",status="404",uri="/"}'
        generated_latency_metrics = b'http_server_requests_seconds_bucket{le="0.005",method="GET",service="Python Microservice with Jaeger",status="200",uri="/metrics"}'
        assert generated_latency_root in generate_latest(self.app.ms.metrics.registry)
        assert generated_latency_metrics in generate_latest(self.app.ms.metrics.registry)

    def test_metrics_count(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_count_root = b'http_server_requests_count_total{method="GET",service="Python Microservice with Jaeger",status="404",uri="/"}'
        generated_count_metrics = b'http_server_requests_count_total{method="GET",service="Python Microservice with Jaeger",status="200",uri="/metrics"}'
        assert generated_count_root in generate_latest(self.app.ms.metrics.registry)
        assert generated_count_metrics in generate_latest(self.app.ms.metrics.registry)

    def test_metrics_logger(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_logger = b'logger_messages_total{level="DEBUG",service="Python Microservice with Jaeger"}'
        assert generated_logger in generate_latest(self.app.ms.metrics.registry)

    def test_metrics_jaeger(self):
        self.client.get("/")
        self.client.get("/metrics")
        generated_logger = b'jaeger:reporter_spans_total'
        assert generated_logger in generate_latest(self.app.ms.metrics.registry)
