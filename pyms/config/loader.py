"""Module to read yaml or json conf"""
import logging
import os

import anyconfig

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME, DEFAULT_CONFIG_FILE
from pyms.exceptions import ConfigDoesNotFoundException
from pyms.utils.utils import AttributeDict

logger = logging.getLogger(LOGGER_NAME)
config_cache = {}


def _normalize_config(config):
    for key, item in config.items():
        if isinstance(item, dict):
            item = dict(_normalize_config(item))
        yield _normalize_keys(key), item


def _normalize_keys(key):
    """The keys will be transformed to a attribute. We need to replace the charactes not valid"""
    key = key.replace("-", "_")
    return key


class ConfigLoader:
    """Recursive get configuration from dictionary, a config file in JSON or YAML format from a path or
    `CONFIGMAP_FILE` environment variable.
    **Atributes:**
    * empty_init: Allow blank variables
    * path: search for config.yml file
    """

    __empty_init = False
    __path = None
    __uppercase = True
    config = None

    def __init__(self, *args, **kwargs):
        """
        Get configuration from a dictionary(variable `config`), from path (variable `path`) or from
        environment with the constant `CONFIGMAP_FILE`
        Set the configuration as upper case to inject the keys in flask config. Flask search for uppercase keys in
        `app.config.from_object`
        ```python
        if key.isupper():
            self[key] = getattr(obj, key)
        ```
        """
        self.__empty_init = kwargs.get("empty_init", False)
        self.__path = kwargs.get("path", None)
        self.__uppercase = kwargs.get("uppercase", True)
        base_config = kwargs.get("config", {})
        if not base_config:
            self.load()
        else:
            self.config = self._transform(base_config)
        #  __import__('pdb').set_trace()
        if not self.config and not self.__empty_init:
            raise ConfigDoesNotFoundException("Configuration file not found")

    def _transform(self, config_src) -> AttributeDict:
        config = dict(_normalize_config(config_src))
        # Flask search for uppercase keys
        if self.__uppercase and "config" in config.get("pyms", {}):
            config["pyms"]["config"] = {k.upper(): v for k, v in config["pyms"]["config"].items()}
        return AttributeDict(config)

    def _get_conf_from_env(self) -> dict:
        self.__path = os.environ.get(CONFIGMAP_FILE_ENVIRONMENT, DEFAULT_CONFIG_FILE)
        logger.debug("[CONF] Searching file in ENV[{}]: {}...".format(CONFIGMAP_FILE_ENVIRONMENT, self.__path))
        return self._get_conf_from_file()

    def _get_conf_from_file(self) -> dict:
        if not self.__path or not os.path.isfile(self.__path):
            logger.debug("[CONF] Configmap {} NOT FOUND".format(self.__path))
            return {}
        if self.__path not in config_cache:
            logger.debug("[CONF] Configmap {} found".format(self.__path))
            config_cache[self.__path] = anyconfig.load(self.__path)
        return config_cache[self.__path]

    def load(self):
        config_src = self._get_conf_from_file() or self._get_conf_from_env()
        self.config = self._transform(config_src)

    def reload(self):
        config_cache.pop(self.__path, None)
        self.load()
