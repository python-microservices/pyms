import logging
import unittest

import os
from pyms.config.confile import ConfFile
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class ConfFromFileEnvTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]

    def test_example_test_file_from_env(self):
        config = ConfFile()
        self.assertEqual(config.my_ms.test_var, "general")


class ConfTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_dictionary_replace_key(self):
        config = ConfFile(config={"test-1": "a", "test_2": "b"})
        self.assertEqual(config.test_1, "a")

    def test_dictionary_normal_key(self):
        config = ConfFile(config={"test-1": "a", "test_2": "b"})
        self.assertEqual(config.test_2, "b")

    def test_dictionary_recursive_dict_replace_key(self):
        config = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "b"})
        self.assertEqual(config.test_1.test_1_1, "a")

    def test_dictionary_recursive_dict_normal_key(self):
        config = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "c"})
        self.assertEqual(config.test_1.test_1_2, "b")

    def test_dictionary_recursive_dict_normal_key_dinamyc(self):
        config = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "c"})
        self.assertEqual(getattr(config, "test_1.test_1_2"), "b")

    def test_dictionary_attribute_not_exists(self):
        config = ConfFile(config={"test-1": "a"})
        with self.assertRaises(AttrDoesNotExistException):
            config.not_exist

    def test_example_test_config_not_exixsts(self):
        with self.assertRaises(ConfigDoesNotFoundException):
            config = ConfFile()

    def test_example_test_file_not_exists(self):
        with self.assertRaises(ConfigDoesNotFoundException):
            config = ConfFile(path="path/not/exist.yml")

    def test_example_test_json_file(self):
        config = ConfFile(path=os.path.join(self.BASE_DIR, "config-tests.json"))
        self.assertEqual(config.my_ms.test_var, "general")
