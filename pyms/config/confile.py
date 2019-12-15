"""Module to read yaml or json conf"""
import logging
import os
from typing import Text

import anyconfig

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException

logger = logging.getLogger(LOGGER_NAME)


class ConfFile(dict):
    """Recursive get configuration from dictionary, a config file in JSON or YAML format from a path or
    `CONFIGMAP_FILE` environment variable.
    **Atributes:**
    * empty_init: Allow blank variables
    * default_file: search for config.yml file
    """
    empty_init = False
    default_file = "config.yml"

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
        self.empty_init = kwargs.get("empty_init", False)
        config = kwargs.get("config")
        uppercase = kwargs.get("uppercase", True)
        if config is None:
            config = self._get_conf_from_file(kwargs.get("path")) or self._get_conf_from_env()

        if not config:
            if self.empty_init:
                config = {}
            else:
                raise ConfigDoesNotFoundException("Configuration file not found")

        config = dict(self.normalize_config(config))
        for k, v in config.items():
            setattr(self, k, v)
            # Flask search for uppercase keys
            if uppercase:
                setattr(self, k.upper(), v)

        super(ConfFile, self).__init__(config)

    def normalize_config(self, config):
        for key, item in config.items():
            if isinstance(item, dict):
                item = ConfFile(config=item, empty_init=self.empty_init)
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
            if self.empty_init:
                return ConfFile(config={}, empty_init=self.empty_init)
            raise AttrDoesNotExistException("Variable {} not exist in the config file".format(name))

    def _get_conf_from_env(self):
        config_file = os.environ.get(CONFIGMAP_FILE_ENVIRONMENT, self.default_file)
        logger.debug("[CONF] Searching file in ENV[{}]: {}...".format(CONFIGMAP_FILE_ENVIRONMENT, config_file))
        return self._get_conf_from_file(config_file)

    @staticmethod
    def _get_conf_from_file(path: Text) -> dict:
        if not path or not os.path.isfile(path):
            return {}
        logger.debug("[CONF] Configmap {} found".format(path))
        conf = anyconfig.load(path)
        return conf

    def __setattr__(self, name, value, *args, **kwargs):
        super(ConfFile, self).__setattr__(name, value)
