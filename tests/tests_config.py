import logging
import os
import unittest

from pyms.config.conf import Config
from pyms.config.confile import ConfFile
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException, ServiceDoesNotExistException

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

    def test_equal_instances_error(self):
        config1 = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}, "test_2": "c"})
        config2 = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}})
        self.assertNotEqual(config1, config2)

    def test_equal_instances_error2(self):
        config1 = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}})
        config2 = {"test-1": {"test-1-1": "a", "test-1-2": "b"}}
        self.assertNotEqual(config1, config2)

    def test_equal_instances_ok(self):
        config1 = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}})
        config2 = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}})
        self.assertEqual(config1, config2)

    def test_equal_instances_ok2(self):
        config1 = ConfFile(config={"test-1": {"test-1-1": "a", "test_1-2": "b"}})
        config2 = {"test_1": {"test_1_1": "a", "test_1_2": "b"}}
        self.assertEqual(config1, config2)

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

    def test_example_test_yaml_file(self):
        config = ConfFile(path=os.path.join(self.BASE_DIR, "config-tests.yml"))
        self.assertEqual(config.my_ms.test_var, "general")

    def test_example_test_json_file(self):
        config = ConfFile(path=os.path.join(self.BASE_DIR, "config-tests.json"))
        self.assertEqual(config.my_ms.test_var, "general")


class ConfServiceTests(unittest.TestCase):

    def test_config_with_service(self):
        class MyService(Config):
            service = "service"

        config = MyService()
        configuration = config.config(config={"service": {"service1": "a", "service2": "b"}})
        self.assertEqual(configuration.service1, "a")

    def test_config_with_service_not_exist(self):
        config = Config()
        with self.assertRaises(ServiceDoesNotExistException):
            configuration = config.config(config={"service": {"service1": "a", "service2": "b"}})


class ConfNotExistTests(unittest.TestCase):
    def test_empty_conf(self):
        config = ConfFile(empty_init=True)
        self.assertEqual(config.my_ms, {})

    def test_empty_conf_two_levels(self):
        config = ConfFile(empty_init=True)
        self.assertEqual(config.my_ms.level_two, {})

    def test_empty_conf_three_levels(self):
        config = ConfFile(empty_init=True)
        self.assertEqual(config.my_ms.level_two.level_three, {})


if __name__ == '__main__':
    unittest.main()
