import logging
import os
import unittest
from unittest import mock

from pyms.config import get_conf, ConfFile
from pyms.config.conf import validate_conf
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, CONFIGMAP_FILE_ENVIRONMENT_LEGACY, LOGGER_NAME, CONFIG_BASE, \
    CRYPT_FILE_KEY_ENVIRONMENT, CRYPT_FILE_KEY_ENVIRONMENT_LEGACY
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException, ServiceDoesNotExistException, \
    ConfigErrorException

logger = logging.getLogger(LOGGER_NAME)


class ConfFromFileEnvTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]

    def test_example_test_file_from_env(self):
        config = ConfFile()
        self.assertEqual(config.pyms.config.test_var, "general")


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

    def test_equal_instances_ko(self):
        config = ConfFile(config={"test-1": {"test-1-1": "a"}})
        no_valid_type = ConfigDoesNotFoundException

        result = config == no_valid_type

        self.assertEqual(result, False)

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
        self.assertEqual(config.pyms.config.test_var, "general")

    def test_example_test_json_file(self):
        config = ConfFile(path=os.path.join(self.BASE_DIR, "config-tests.json"))
        self.assertEqual(config.pyms.config.test_var, "general")


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


class GetConfig(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT] = os.path.join(self.BASE_DIR, "config-tests.yml")

    def tearDown(self):
        del os.environ[CONFIGMAP_FILE_ENVIRONMENT]

    def test_default(self):
        config = get_conf(service=CONFIG_BASE, uppercase=True)
        assert config.app_name == "Python Microservice"
        assert config.subservice1.test == "input"

    def test_default_flask(self):
        config = get_conf(service=CONFIG_BASE, uppercase=True).to_flask()
        assert config.APP_NAME == "Python Microservice"
        assert config.SUBSERVICE1.test == "input"

    @mock.patch('pyms.config.conf.ConfFile')
    def test_without_params(self, mock_confile):
        with self.assertRaises(ServiceDoesNotExistException):
            get_conf()


class ConfValidateTests(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def tearDown(self):
        if os.getenv(CONFIGMAP_FILE_ENVIRONMENT) is not None:
            del os.environ[CONFIGMAP_FILE_ENVIRONMENT]
        if os.getenv(CONFIGMAP_FILE_ENVIRONMENT_LEGACY) is not None:
            del os.environ[CONFIGMAP_FILE_ENVIRONMENT_LEGACY]
        if os.getenv(CRYPT_FILE_KEY_ENVIRONMENT) is not None:
            del os.environ[CRYPT_FILE_KEY_ENVIRONMENT]
        if os.getenv(CRYPT_FILE_KEY_ENVIRONMENT_LEGACY) is not None:
            del os.environ[CRYPT_FILE_KEY_ENVIRONMENT_LEGACY]

    def test_wrong_block_no_pyms(self):
        with self.assertRaises(ConfigErrorException):
            validate_conf(path=os.path.join(self.BASE_DIR, "config-tests-bad-structure.yml"))

    def test_wrong_block_no_config(self):
        with self.assertRaises(ConfigErrorException):
            validate_conf(path=os.path.join(self.BASE_DIR, "config-tests-bad-structure2.yml"))

    def test_wrong_block_not_valid_structure(self):
        with self.assertRaises(ConfigErrorException):
            validate_conf(path=os.path.join(self.BASE_DIR, "config-tests-bad-structure3.yml"))

    def test_validate_conf_file_with_env_deprecated(self):
        self.all_validate_conf_combinations(True)

    def test_validate_conf_file_with_env_deprecated_and_updated(self):
        os.environ[CONFIGMAP_FILE_ENVIRONMENT_LEGACY] = os.path.join(self.BASE_DIR, "config-tests-deprecated.yml")
        self.all_validate_conf_combinations()

    def test_validate_crypt_file_with_env_deprecated(self):
        os.environ[CRYPT_FILE_KEY_ENVIRONMENT_LEGACY] = os.path.join(self.BASE_DIR, "key.key")
        self.all_validate_conf_combinations()

    def test_validate_crypt_file_with_env_deprecated_and_updated(self):
        os.environ[CRYPT_FILE_KEY_ENVIRONMENT] = os.path.join(self.BASE_DIR, "key.key")
        os.environ[CRYPT_FILE_KEY_ENVIRONMENT_LEGACY] = os.path.join(self.BASE_DIR, "key_deprecated.key")
        self.all_validate_conf_combinations()

    def all_validate_conf_combinations(self, legacy=False):
        config_env = CONFIGMAP_FILE_ENVIRONMENT
        if legacy:
            config_env = CONFIGMAP_FILE_ENVIRONMENT_LEGACY
        os.environ[config_env] = os.path.join(self.BASE_DIR, "config-tests.yml")
        validate_conf()
        os.environ[config_env] = os.path.join(self.BASE_DIR, "config-tests-debug.yml")
        validate_conf()
        os.environ[config_env] = os.path.join(self.BASE_DIR, "config-tests-debug-off.yml")
        validate_conf()
