import os
import unittest

from flask import current_app

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, SERVICE_ENVIRONMENT
from pyms.flask.app import Microservice, config


def home():
    current_app.logger.info("start request")
    return "OK"


class MyMicroservice(Microservice):
    pass


class MicroserviceTest(unittest.TestCase):
    """
    Tests for healthcheack endpoints
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests.yml")
        os.environ[SERVICE_ENVIRONMENT] = "my-ms"


    def test_singleton(self):
        ms1 = Microservice(service="my-ms", path=__file__)
        ms2 = Microservice(service="my-ms", path=__file__)
        self.assertEqual(ms1, ms2)

    def test_singleton_child_class(self):
        ms1 = Microservice(service="my-ms", path=__file__)
        ms2 = MyMicroservice()
        self.assertNotEqual(ms1, ms2)

    def test_singleton_inherit_conf(self):
        ms1 = Microservice(service="my-ms", path=__file__)
        ms2 = MyMicroservice()
        self.assertEqual(ms1.config.subservice1, ms2.config.subservice1)

    def test_import_config_without_create_app(self):
        ms1 = MyMicroservice(service="my-ms", path=__file__, override_instance=True)
        self.assertEqual(ms1.config.subservice1, config().subservice1)


class HomeTests(unittest.TestCase):
    """
    Tests for healthcheack endpoints
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests.yml")
        ms = Microservice(service="my-ms", path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(200, response.status_code)

    def test_error(self):
        response = self.client.get('/notexist')
        self.assertEqual(404, response.status_code)
