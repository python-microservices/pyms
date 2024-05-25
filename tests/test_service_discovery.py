"""Test common rest operations wrapper.
"""

import os
import unittest
from unittest.mock import patch

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice
from pyms.flask.services.service_discovery import ServiceDiscoveryBase, ServiceDiscoveryConsul


class MockServiceDiscovery(ServiceDiscoveryBase):
    pass


class ServiceDiscoveryConsulTests(unittest.TestCase):
    """Test service discovery services"""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(
            self.BASE_DIR, "config-tests-service-discovery-consul.yml"
        )
        ms = Microservice(path=__file__)
        self.ms = ms

    @patch.object(ServiceDiscoveryConsul, "register_service", return_value=None)
    def test_init(self, mock_consul):
        """test if the initializacion of service discovery call to the Service Discovery server to autoregister"""
        self.ms.create_app()

        mock_consul.assert_called_once_with(
            app_name="Python Microservice Service Discovery",
            healtcheck_url="http://127.0.0.1.nip.io:5000/healthcheck",
            interval="10s",
        )

    def test_get_client(self):
        client = self.ms.service_discovery.get_client()

        self.assertTrue(isinstance(client, ServiceDiscoveryConsul))


class ServiceDiscoveryTests(unittest.TestCase):
    """Test service discovery services"""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-service-discovery.yml")
        ms = Microservice(path=__file__)
        ms.reload_conf()
        self.ms = ms

    def test_get_client(self):
        self.ms.create_app()
        client = self.ms.service_discovery.get_client()

        self.assertTrue(isinstance(client, MockServiceDiscovery))
