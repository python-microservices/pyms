"""Module to read yaml conf"""
import logging
import os

from typing import Text

import yaml

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException

logger = logging.getLogger(LOGGER_NAME)


class ConfFile(dict):
    def __init__(self, *args, **kwargs):
        """
        Get configuration from a dictionary(variable `config`), from path (variable `path`) or from
        environment with the constant `CONFIGMAP_FILE_ENVIRONMENT`
        """

        config = kwargs.get("config") or self._get_conf_from_yaml_file(kwargs.get("path")) or self._get_conf_from_env()

        if not config:
            raise ConfigDoesNotFoundException("Configuration file not found")

        logger.debug("[CONF] INIT: Settings {kwargs}".format(
            kwargs=kwargs,
        ))

        config = {k: v for k, v in self.normalize_config(config)}
        [setattr(self, k, v) for k, v in config.items()]
        super(ConfFile, self).__init__(config)

    def normalize_config(self, config):
        for key, item in config.items():
            if isinstance(item, dict):
                item = ConfFile(config=item)
            yield self.normalize_keys(key), item

    def normalize_keys(self, key):
        """The keys will be transformed to a attribute. We need to replace the charactes not valid"""
        key = key.replace("-", "_")
        return key

    def __getattr__(self, name, *args, **kwargs):
        try:
            keys = self.normalize_keys(name).split(".")
            aux_dict = self
            for k in keys:
                aux_dict = aux_dict[k]
            return aux_dict
        except KeyError:
            raise AttrDoesNotExistException("Variable {} not exist in the config file".format(name))

    def _get_conf_from_env(self):
        file = os.environ.get(CONFIGMAP_FILE_ENVIRONMENT)
        logger.info("[CONF] Searching file in ENV[{}]: {}...".format(CONFIGMAP_FILE_ENVIRONMENT, file))
        return self._get_conf_from_yaml_file(os.environ.get(CONFIGMAP_FILE_ENVIRONMENT))

    def _get_conf_from_yaml_file(self, path: Text) -> dict:
        if not path or not os.path.isfile(path):
            return {}
        logger.info("[CONF] Configmap {} found".format(path))
        f = open(path, "r")
        conf = self._get_conf_from_yaml(f.read())
        f.close()
        return conf

    def _get_conf_from_yaml(self, config: Text) -> dict:
        return yaml.safe_load(config)

    def __setattr__(self, name, value, *args, **kwargs):
        super(ConfFile, self).__setattr__(name, value)
