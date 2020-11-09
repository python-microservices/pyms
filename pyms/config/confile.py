"""Module to read yaml or json conf"""
import logging
import os
import re
from typing import Dict, Iterable, Text, Tuple, Union

import anyconfig

from pyms.constants import (
    CONFIGMAP_FILE_ENVIRONMENT,
    CONFIGMAP_FILE_ENVIRONMENT_LEGACY,
    DEFAULT_CONFIGMAP_FILENAME,
    LOGGER_NAME,
)
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException
from pyms.utils.files import LoadFile

logger = logging.getLogger(LOGGER_NAME)


class ConfFile(dict):
    """Recursive get configuration from dictionary, a config file in JSON or YAML format from a path or
    `PYMS_CONFIGMAP_FILE` environment variable.
    **Atributes:**
    * path: Path to find the `DEFAULT_CONFIGMAP_FILENAME` and `DEFAULT_KEY_FILENAME` if use encrypted vars
    * empty_init: Allow blank variables
    * config: Allow to pass a dictionary to ConfFile without use a file
    """

    _empty_init = False
    _crypt = None

    def __init__(self, *args, **kwargs):
        """
        Get configuration from a dictionary(variable `config`), from path (variable `path`) or from
        environment with the constant `PYMS_CONFIGMAP_FILE`
        Set the configuration as upper case to inject the keys in flask config. Flask search for uppercase keys in
        `app.config.from_object`
        ```python
        if key.isupper():
            self[key] = getattr(obj, key)
        ```
        """
        # TODO Remove temporally backward compatibility on future versions
        configmap_file_env = self.__get_updated_configmap_file_env()  # Temporally backward compatibility

        self._loader = LoadFile(kwargs.get("path"), configmap_file_env, DEFAULT_CONFIGMAP_FILENAME)
        self._crypt_cls = kwargs.get("crypt")
        if self._crypt_cls:
            self._crypt = self._crypt_cls(path=kwargs.get("path"))
        self._empty_init = kwargs.get("empty_init", False)
        config = kwargs.get("config")
        if config is None:
            config = self._loader.get_file(anyconfig.load)
        if not config:
            if self._empty_init:
                config = {}
            else:
                path = self._loader.path if self._loader.path else ""
                raise ConfigDoesNotFoundException("Configuration file {}not found".format(path + " "))

        config = self.set_config(config)

        super().__init__(config)

    def to_flask(self) -> Dict:
        return ConfFile(config={k.upper(): v for k, v in self.items()}, crypt=self._crypt_cls)

    def set_config(self, config: Dict) -> Dict:
        """
        Set a dictionary as attributes of ConfFile. This attributes could be access as `ConfFile["attr"]` or
        ConfFile.attr
        :param config: a dictionary from `config.yml`
        :return:
        """
        config = dict(self.normalize_config(config))
        pop_encripted_keys = []
        add_decripted_keys = []
        for k, v in config.items():
            if k.lower().startswith("enc_"):
                k_not_crypt = re.compile(re.escape("enc_"), re.IGNORECASE)
                decrypted_key = k_not_crypt.sub("", k)
                decrypted_value = self._crypt.decrypt(v) if self._crypt else None
                setattr(self, decrypted_key, decrypted_value)
                add_decripted_keys.append((decrypted_key, decrypted_value))
                pop_encripted_keys.append(k)
            else:
                setattr(self, k, v)

        # Delete encrypted keys to prevent decrypt multiple times a element
        for x in pop_encripted_keys:
            config.pop(x)

        for k, v in add_decripted_keys:
            config[k] = v

        return config

    def normalize_config(self, config: Dict) -> Iterable[Tuple[Text, Union[Dict, Text, bool]]]:
        for key, item in config.items():
            if isinstance(item, dict):
                item = ConfFile(config=item, empty_init=self._empty_init, crypt=self._crypt_cls)
            yield self.normalize_keys(key), item

    @staticmethod
    def normalize_keys(key: Text) -> Text:
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
        except KeyError as e:
            if self._empty_init:
                return ConfFile(config={}, empty_init=self._empty_init, crypt=self._crypt_cls)
            raise AttrDoesNotExistException("Variable {} not exist in the config file".format(name)) from e

    def reload(self):
        """
        Remove file from memoize variable, return again the content of the file and set the configuration again
        :return: None
        """
        config_src = self._loader.reload(anyconfig.load)
        self.set_config(config_src)

    def __setattr__(self, name, value, *args, **kwargs):
        super().__setattr__(name, value)

    @staticmethod
    def __get_updated_configmap_file_env() -> str:
        result = CONFIGMAP_FILE_ENVIRONMENT
        if (os.getenv(CONFIGMAP_FILE_ENVIRONMENT_LEGACY) is not None) and (
            os.getenv(CONFIGMAP_FILE_ENVIRONMENT) is None
        ):
            result = CONFIGMAP_FILE_ENVIRONMENT_LEGACY
        return result
