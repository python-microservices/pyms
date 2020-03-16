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
        response = self.client.get('/test-api-path/ws-doc/')
        self.assertEqual(200, response.status_code)

    def test_home(self):
        response = self.client.get('/test-api-path/')
        self.assertEqual(200, response.status_code)


class SwaggerNoAbsPathTests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-swagger_no_abs_path.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice Swagger2", self.app.config["APP_NAME"])

    def test_default(self):
        response = self.client.get('/test-api-path2/ws-doc2/')
        self.assertEqual(200, response.status_code)

    def test_home(self):
        response = self.client.get('/test-api-path2/no-abs-path')
        self.assertEqual(200, response.status_code)


class SwaggerOpenapi3Tests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-swagger_3.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice Swagger Openapi 3", self.app.config["APP_NAME"])

    def test_default(self):
        response = self.client.get('/ws-doc/')
        self.assertEqual(200, response.status_code)

    def test_home(self):
        response = self.client.get('/test-url')
        self.assertEqual(200, response.status_code)


class SwaggerOpenapi3NoAbsPathTests(unittest.TestCase):
    """Test common rest operations wrapper.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-swagger_3_no_abs_path.yml")
        ms = MyMicroserviceNoSingleton(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice Swagger Openapi 3 No abspath", self.app.config["APP_NAME"])

    def test_default(self):
        response = self.client.get('/test-api-path2/ws-doc2/')
        self.assertEqual(200, response.status_code)

    def test_home(self):
        response = self.client.get('/test-api-path2/test-url')
        self.assertEqual(200, response.status_code)
