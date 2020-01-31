"""Test common rest operations wrapper.
"""
import os
import unittest

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from tests.common import MyMicroserviceNoSingleton


class SwaggerTests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-swagger.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice Swagger", self.app.config["APP_NAME"])

    def test_default(self):
        response = self.client.get('/ws-doc/')
        self.assertEqual(200, response.status_code)
