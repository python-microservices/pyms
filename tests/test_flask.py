import os
import unittest

import pytest
from flask import current_app

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice, config
from pyms.flask.services.driver import DriverService
from tests.common import MyMicroservice


def home():
    current_app.logger.info("start request")
    return "OK2"


class HomeWithFlaskTests(unittest.TestCase):
    """
    Tests for healthcheack endpoints
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config-tests-flask.yml"
        )
        ms = MyMicroservice()
        ms.reload_conf()
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("Python Microservice With Flask", self.app.config["APP_NAME"])

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(404, response.status_code)

    def test_healthcheck(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(b"OK", response.data)
        self.assertEqual(200, response.status_code)

    def test_swagger(self):
        response = self.client.get("/ui/")
        self.assertEqual(404, response.status_code)


class FlaskWithSwaggerTests(unittest.TestCase):
    """
    Tests for healthcheack endpoints
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config-tests-flask-swagger.yml"
        )
        ms = MyMicroservice(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.connexion_app.test_client()
        self.assertEqual("Python Microservice With Flask in tests", self.app.config["APP_NAME"])

    def test_healthcheck(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(b"OK", response.content)
        self.assertEqual(200, response.status_code)

    def test_swagger(self):
        response = self.client.get("/ui/")
        self.assertEqual(200, response.status_code)

    def test_exists_service(self):
        self.assertTrue(isinstance(self.app.ms.swagger, DriverService))

    # def test_reverse_proxy(self):
    #     response = self.client.get("/my-proxy-path/ui/", headers={"X-Script-Name": "/my-proxy-path"})
    #     self.assertEqual(200, response.status_code)
    #
    # def test_reverse_proxy_no_slash(self):
    #     response = self.client.get("/my-proxy-path/ui/", headers={"X-Script-Name": "my-proxy-path"})
    #     self.assertEqual(200, response.status_code)
    #
    # def test_reverse_proxy_zuul(self):
    #     response = self.client.get("/my-proxy-path-zuul/ui/", headers={"X-Forwarded-Prefix": "my-proxy-path-zuul"})
    #     self.assertEqual(200, response.status_code)


class ReloadTests(unittest.TestCase):
    """
    Tests for configreload endpoints
    """

    file1 = "config-tests-reload1.yml"
    file2 = "config-tests-reload2.yml"

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file1)
        ms = MyMicroservice(path=__file__)
        self.app = ms.create_app()
        self.client = self.app.test_client()
        self.assertEqual("reload1", self.app.config["APP_NAME"])

    def test_configreload(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file2)
        response = self.client.post("/reload-config")
        self.assertEqual(b"OK", response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("reload2", config()["APP_NAME"])


class MicroserviceTest(unittest.TestCase):
    """
    Tests for Singleton
    """

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config-tests.yml"
        )

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


@pytest.mark.parametrize(
    "payload, configfile, status_code",
    [
        # ("Python Microservice", "config-tests.yml", 200),
        ("Python Microservice With Flask", "config-tests-flask.yml", 404),
        # ("Python Microservice With Flask and Lightstep", "config-tests-flask-trace-lightstep.yml", 200),
    ],
)
def test_configfiles(payload, configfile, status_code):
    os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(os.path.dirname(os.path.abspath(__file__)), configfile)
    ms = MyMicroservice(path=__file__)
    ms.reload_conf()
    app = ms.create_app()
    client = app.test_client()
    response = client.get("/")
    assert payload == app.config["APP_NAME"]
    assert status_code == response.status_code
