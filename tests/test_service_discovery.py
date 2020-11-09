"""Test common rest operations wrapper.
"""
import os
import unittest

import requests_mock

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice
from pyms.flask.services.service_discovery import ServiceDiscoveryConsul


class ServiceDiscoveryTests(unittest.TestCase):
    """Test common rest operations wrapper."""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests-service-discovery.yml")
        ms = Microservice(path=__file__)
        self.ms = ms

    @requests_mock.Mocker()
    def test_init(self, mock_request):
        url = "http://localhost:8500/v1/agent/check/register"

        mock_request.put(url)
        self.ms.create_app()

        self.assertTrue(True)

    def test_get_client(self):
        client = self.ms.service_discovery.get_client()

        self.assertTrue(isinstance(client, ServiceDiscoveryConsul))
