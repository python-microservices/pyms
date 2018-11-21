import logging
import os
import unittest
import sys

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT
from pyms.flask.app import Microservice


class TracerTest(unittest.TestCase):

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config-tests.yml"
        )
        self.ms = Microservice(service="my-ms", path=__file__)
        self.app = self.ms.create_app()
        self.client = self.app.test_client()
        self.stream_handler = logging.StreamHandler(sys.stdout)

    def test_using_info_level(self):
        expected_result = ['INFO:flask.app:SendingData']
        self.app.logger.addHandler(self.stream_handler)
        with self.assertLogs(level='INFO') as cm:
            with self.app.app_context():
                self.app.logger.info("SendingData")
        self.assertEqual(expected_result, cm.output)

    def exception_raiser(self):
        raise ZeroDivisionError

    def test_raising_exception(self):
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.app.logger.addHandler(self.stream_handler)
        with self.assertLogs(level='ERROR') as cm:
            with self.app.app_context():
                with self.assertRaises(ZeroDivisionError) as context:
                    self.app.logger.error("DivisionByZero")
                    self.exception_raiser()
                    self.assertEqual('division by zero', str(context.exception))
        self.assertEqual(cm.output, ['ERROR:flask.app:DivisionByZero'])

    def tearDown(self):
        self.app.logger.removeHandler(self.stream_handler)
