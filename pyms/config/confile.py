"""Module to read yaml or json conf"""
import logging
import os

import anyconfig

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException

logger = logging.getLogger(LOGGER_NAME)

config_cache = {}


class ConfFile(dict):
    """Recursive get configuration from dictionary, a config file in JSON or YAML format from a path or
    `CONFIGMAP_FILE` environment variable.
    **Atributes:**
    * empty_init: Allow blank variables
    * default_file: search for config.yml file
    """
    _empty_init = False
    _default_file = "config.yml"
    __path = None

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
        self._empty_init = kwargs.get("empty_init", False)
        config = kwargs.get("config")
        if config is None:
            self.set_path(kwargs.get("path"))
            config = self._get_conf_from_file() or self._get_conf_from_env()

        if not config:
            if self._empty_init:
                config = {}
            else:
                raise ConfigDoesNotFoundException("Configuration file not found")

        config = self.set_config(config)

        super(ConfFile, self).__init__(config)

    def set_path(self, path):
        self.__path = path

    def to_flask(self):
        return ConfFile(config={k.upper(): v for k, v in self.items()})

    def set_config(self, config):
        config = dict(self.normalize_config(config))
        for k, v in config.items():
            setattr(self, k, v)
        return config

    def normalize_config(self, config):
        for key, item in config.items():
            if isinstance(item, dict):
                item = ConfFile(config=item, empty_init=self._empty_init)
            yield self.normalize_keys(key), item

    @staticmethod
    def normalize_keys(key):
        """The keys will be transformed to a attribute. We need to replace the charactes not valid"""
        key = key.replace("-", "_")
        return key

    def __eq__(self, other):
        if not isinstance(other, ConfFile) and not isinstance(other, dict):
            return False
        return dict(self) == dict(other)

    def __getattr__(self, name, *args, **kwargs):
        try:
            keys = self.normalize_keys(name).split(".")
            aux_dict = self
            for k in keys:
                aux_dict = aux_dict[k]
            return aux_dict
        except KeyError:
            if self._empty_init:
                return ConfFile(config={}, empty_init=self._empty_init)
            raise AttrDoesNotExistException("Variable {} not exist in the config file".format(name))

    def _get_conf_from_env(self):
        config_file = os.environ.get(CONFIGMAP_FILE_ENVIRONMENT, self._default_file)
        logger.debug("[CONF] Searching file in ENV[{}]: {}...".format(CONFIGMAP_FILE_ENVIRONMENT, config_file))
        self.set_path(config_file)
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
        self.set_config(config_src)

    def reload(self):
        config_cache.pop(self.__path, None)
        self.load()

    def __setattr__(self, name, value, *args, **kwargs):
        super(ConfFile, self).__setattr__(name, value)
