import logging
import os
import unittest
from unittest import mock

from pyms.config import get_conf, ConfigLoader
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME, CONFIG_BASE
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException, ServiceDoesNotExistException

logger = logging.getLogger(LOGGER_NAME)


class ConfFromFileEnvTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]

    def test_example_test_file_from_env(self):
        config = ConfigLoader().config
        self.assertEqual(config.pyms.config.TEST_VAR, "general")


class ConfTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_dictionary_replace_key(self):
        config = ConfigLoader(config={"test-1": "a", "test_2": "b"}).config
        self.assertEqual(config.test_1, "a")

    def test_dictionary_normal_key(self):
        config = ConfigLoader(config={"test-1": "a", "test_2": "b"}).config
        self.assertEqual(config.test_2, "b")

    def test_dictionary_recursive_dict_replace_key(self):
        config = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "b"}).config
        self.assertEqual(config.test_1.test_1_1, "a")

    def test_dictionary_recursive_dict_normal_key(self):
        config = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "c"}).config
        self.assertEqual(config.test_1.test_1_2, "b")

    def test_equal_instances_error(self):
        config1 = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "c"}).config
        config2 = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}}).config
        self.assertNotEqual(config1, config2)

    def test_equal_instances_error2(self):
        config1 = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}}).config
        config2 = {"test-1": {"test-1-1": "a", "test-1-2": "b"}}
        self.assertNotEqual(config1, config2)

    def test_equal_instances_ok(self):
        config1 = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}}).config
        config2 = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}}).config
        self.assertEqual(config1, config2)

    def test_equal_instances_ok2(self):
        config1 = ConfigLoader(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}}).config
        config2 = {"test_1": {"test_1_1": "a", "test_1_2": "b"}}
        self.assertEqual(config1, config2)

    def test_equal_instances_ko(self):
        config = ConfigLoader(config={"test-1": {"test-1-1": "a"}}).config
        no_valid_type = ConfigDoesNotFoundException

        result = config == no_valid_type

        self.assertEqual(result, False)

    def test_dictionary_attribute_not_exists(self):
        config = ConfigLoader(config={"test-1": "a"}).config
        with self.assertRaises(KeyError):
            config.not_exist

    def test_example_test_config_not_exixsts(self):
        with self.assertRaises(ConfigDoesNotFoundException):
            ConfigLoader()

    def test_example_test_file_not_exists(self):
        with self.assertRaises(ConfigDoesNotFoundException):
            ConfigLoader(path="path/not/exist.yml")

    def test_example_test_yaml_file(self):
        config = ConfigLoader(path=os.path.join(self.BASE_DIR, "config-tests.yml")).config
        self.assertEqual(config.pyms.config.TEST_VAR, "general")

    def test_example_test_json_file(self):
        config = ConfigLoader(path=os.path.join(self.BASE_DIR, "config-tests.json")).config
        self.assertEqual(config.pyms.config.TEST_VAR, "general")


class GetConfig(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]

    def test_default(self):
        config = get_conf(service=CONFIG_BASE)
        assert config.APP_NAME == "Python Microservice"
        assert config.SUBSERVICE1.test == "input"

    @mock.patch('pyms.config.config.ConfigLoader')
    def test_without_params(self, mock_confile):
        with self.assertRaises(ServiceDoesNotExistException):
            get_conf()
