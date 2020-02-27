"""Module to read yaml or json conf"""
import logging
import re
from typing import Dict, Union, Text, Tuple, Iterable

import anyconfig

from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, LOGGER_NAME, DEFAULT_CONFIGMAP_FILENAME
from pyms.exceptions import AttrDoesNotExistException, ConfigDoesNotFoundException
from pyms.utils.crypt import Crypt
from pyms.utils.files import LoadFile

logger = logging.getLogger(LOGGER_NAME)


class ConfFile(dict):
    """Recursive get configuration from dictionary, a config file in JSON or YAML format from a path or
    `CONFIGMAP_FILE` environment variable.
    **Atributes:**
    * path: Path to find the `DEFAULT_CONFIGMAP_FILENAME` and `DEFAULT_KEY_FILENAME` if use encrypted vars
    * empty_init: Allow blank variables
    * config: Allow to pass a dictionary to ConfFile without use a file
    """
    _empty_init = False

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
        self._loader = LoadFile(kwargs.get("path"), CONFIGMAP_FILE_ENVIRONMENT, DEFAULT_CONFIGMAP_FILENAME)
        self._crypt = Crypt(path=kwargs.get("path"))
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

        super(ConfFile, self).__init__(config)

    def to_flask(self) -> Dict:
        return ConfFile(config={k.upper(): v for k, v in self.items()})

    def set_config(self, config: Dict) -> Dict:
        """
        Set a dictionary as attributes of ConfFile. This attributes could be access as `ConfFile["attr"]` or
        ConfFile.attr
        :param config: a dictionary from `config.yml`
        :return:
        """
        config = dict(self.normalize_config(config))
        pop_encripted_keys = []
        for k, v in config.items():
            if k.lower().startswith("enc_"):
                k_not_crypt = re.compile(re.escape('enc_'), re.IGNORECASE)
                setattr(self, k_not_crypt.sub('', k), self._crypt.decrypt(v))
                pop_encripted_keys.append(k)
            else:
                setattr(self, k, v)

        # Delete encrypted keys to prevent decrypt multiple times a element
        for x in pop_encripted_keys:
            config.pop(x)

        return config

    def normalize_config(self, config: Dict) -> Iterable[Tuple[Text, Union[Dict, Text, bool]]]:
        for key, item in config.items():
            if isinstance(item, dict):
                item = ConfFile(config=item, empty_init=self._empty_init)
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
        except KeyError:
            if self._empty_init:
                return ConfFile(config={}, empty_init=self._empty_init)
            raise AttrDoesNotExistException("Variable {} not exist in the config file".format(name))

    def reload(self):
        """
        Remove file from memoize variable, return again the content of the file and set the configuration again
        :return: None
        """
        config_src = self._loader.reload(anyconfig.load)
        self.set_config(config_src)

    def __setattr__(self, name, value, *args, **kwargs):
        super(ConfFile, self).__setattr__(name, value)
