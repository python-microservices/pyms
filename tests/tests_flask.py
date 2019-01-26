import os
import unittest

from flask import current_app

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice


def home():
    current_app.logger.info("start request")
    return "OK"


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
