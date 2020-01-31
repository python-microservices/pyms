import os
import unittest

import pytest
from flask import current_app

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice, config
from pyms.flask.services.driver import DriverService
from tests.common import MyMicroserviceNoSingleton, MyMicroservice


def home():
    current_app.logger.info("start request")
    return "OK"


class HomeWithFlaskTests(unittest.TestCase):
    """
    Tests for healthcheack endpoints
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests-flask.yml")
        ms = MyMicroservice(path=__file__)
        ms.reload_conf()
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice With Flask", self.app.config["APP_NAME"])

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(404, response.status_code)

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(b"OK", response.data)
        self.assertEqual(200, response.status_code)

    def test_swagger(self):
        response = self.client.get('/ui/')
        self.assertEqual(404, response.status_code)


class FlaskWithSwaggerTests(unittest.TestCase):
    """
    Tests for healthcheack endpoints
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests-flask-swagger.yml")
        ms = MyMicroservice(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice With Flask", self.app.config["APP_NAME"])

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(b"OK", response.data)
        self.assertEqual(200, response.status_code)

    def test_swagger(self):
        response = self.client.get('/ui/')
        self.assertEqual(200, response.status_code)

    def test_exists_service(self):
        self.assertTrue(isinstance(self.app.ms.swagger, DriverService))

    def test_disabled_service(self):
        with pytest.raises(AttributeError) as excinfo:
            self.assertTrue(isinstance(self.app.ms.metrics, DriverService))
        assert "'MyMicroservice' object has no attribute 'metrics'" in str(excinfo.value)


class MicroserviceTest(unittest.TestCase):
    """
    Tests for Singleton
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              "config-tests.yml")

    def test_singleton(self):
        ms1 = Microservice(path=__file__)
        ms2 = Microservice(path=__file__)
        self.assertEqual(ms1, ms2)

    def test_singleton_child_class(self):
        ms1 = Microservice(path=__file__)
        ms2 = MyMicroservice()
        self.assertNotEqual(ms1, ms2)

    def test_singleton_inherit_conf(self):
        ms1 = Microservice(path=__file__)
        ms2 = MyMicroservice()
        self.assertEqual(ms1.config.subservice1, ms2.config.subservice1)

    def test_import_config_without_create_app(self):
        ms1 = MyMicroservice(path=__file__)
        self.assertEqual(ms1.config.subservice1, config().subservice1)

    def test_config_singleton(self):
        conf_one = config().subservice1
        conf_two = config().subservice1

        assert conf_one == conf_two


@pytest.mark.parametrize("payload, configfile, status_code", [
    (
            "Python Microservice",
            "config-tests.yml",
            200
    ),
    (
            "Python Microservice With Flask",
            "config-tests-flask.yml",
            404
    ),
    (
            "Python Microservice With Flask and Lightstep",
            "config-tests-flask-trace-lightstep.yml",
            200
    )
])
def test_configfiles(payload, configfile, status_code):
    os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                          configfile)
    ms = MyMicroservice(path=__file__)
    ms.reload_conf()
    app = ms.create_app()
    client = app.test_client()
    response = client.get('/')
    assert payload == app.config["APP_NAME"]
    assert status_code == response.status_code
