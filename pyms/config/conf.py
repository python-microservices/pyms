import logging
import os
from typing import Union

import yaml

from pyms.config.confile import ConfFile
from pyms.constants import (
    CONFIGMAP_FILE_ENVIRONMENT,
    CONFIGMAP_FILE_ENVIRONMENT_LEGACY,
    CRYPT_FILE_KEY_ENVIRONMENT,
    CRYPT_FILE_KEY_ENVIRONMENT_LEGACY,
    DEFAULT_CONFIGMAP_FILENAME,
    LOGGER_NAME,
    PYMS_CONFIG_WHITELIST_KEYWORDS,
)
from pyms.exceptions import AttrDoesNotExistException, ConfigErrorException, ServiceDoesNotExistException
from pyms.utils import utils

logger = logging.getLogger(LOGGER_NAME)


def get_conf(*args, **kwargs):
    """
    Returns an object with a set of attributes retrieved from the configuration file. Each subblock is a append of the
    parent and this name, in example of the next yaml, tracer will be `pyms.tracer`. If we have got his config file:
    See these docs:
    * https://python-microservices.github.io/configuration/
    * https://python-microservices.github.io/services/
    :param args:
    :param kwargs:

    :return:
    """
    service = kwargs.pop("service", None)
    if not service:
        raise ServiceDoesNotExistException("Service not defined")
    config = ConfFile(*args, **kwargs)
    return getattr(config, service)


def validate_conf(*args, **kwargs):

    config = ConfFile(*args, **kwargs)
    is_config_ok = True
    try:
        config.pyms
    except AttrDoesNotExistException:
        is_config_ok = False
    if not is_config_ok:
        raise ConfigErrorException(
            """Config file must start with `pyms` keyword, for example:
    pyms:
      services:
        metrics: true
        requests:
          data: data
        swagger:
          path: ""
          file: "swagger.yaml"
        tracer:
          client: "jaeger"
          host: "localhost"
          component_name: "Python Microservice"
      config:
        DEBUG: true
        TESTING: true"""
        )
    try:
        config.pyms.config
    except AttrDoesNotExistException:
        is_config_ok = False
    if not is_config_ok:
        raise ConfigErrorException(
            """`pyms` block must contain a `config` keyword in your Config file, for example:
    pyms:
      services:
        metrics: true
        requests:
          data: data
        swagger:
          path: ""
          file: "swagger.yaml"
        tracer:
          client: "jaeger"
          host: "localhost"
          component_name: "Python Microservice"
      config:
        DEBUG: true
        TESTING: true"""
        )
    wrong_keywords = [i for i in config.pyms if i not in PYMS_CONFIG_WHITELIST_KEYWORDS]
    if len(wrong_keywords) > 0:
        raise ConfigErrorException(
            """{} isn`t a valid keyword for pyms block, for example:
        pyms:
          services:
            metrics: true
            requests:
              data: data
            swagger:
              path: ""
              file: "swagger.yaml"
            tracer:
              client: "jaeger"
              host: "localhost"
              component_name: "Python Microservice"
          config:
            DEBUG: true
            TESTING: true""".format(
                wrong_keywords
            )
        )

    # TODO Remove temporally deprecated warnings on future versions
    __verify_deprecated_env_variables(config)


def __verify_deprecated_env_variables(config):
    env_var_duplicated = 'IMPORTANT: If you are using "{}" environment variable, "{}" value will be ignored.'
    env_var_deprecated = 'IMPORTANT: "{}" environment variable is deprecated on this version, use "{}" instead.'

    if os.getenv(CONFIGMAP_FILE_ENVIRONMENT_LEGACY) is not None:
        if os.getenv(CONFIGMAP_FILE_ENVIRONMENT) is not None:
            msg = env_var_duplicated.format(CONFIGMAP_FILE_ENVIRONMENT, CONFIGMAP_FILE_ENVIRONMENT_LEGACY)
        else:
            msg = env_var_deprecated.format(CONFIGMAP_FILE_ENVIRONMENT_LEGACY, CONFIGMAP_FILE_ENVIRONMENT)
        try:
            if config.pyms.config.DEBUG:
                msg = utils.colored_text(msg, utils.Colors.BRIGHT_YELLOW, True)
        except AttrDoesNotExistException:
            pass
        logger.warning(msg)

    if os.getenv(CRYPT_FILE_KEY_ENVIRONMENT_LEGACY) is not None:
        if os.getenv(CRYPT_FILE_KEY_ENVIRONMENT) is not None:
            msg = env_var_duplicated.format(CRYPT_FILE_KEY_ENVIRONMENT, CRYPT_FILE_KEY_ENVIRONMENT_LEGACY)
        else:
            msg = env_var_deprecated.format(CRYPT_FILE_KEY_ENVIRONMENT_LEGACY, CRYPT_FILE_KEY_ENVIRONMENT)
        try:
            if config.pyms.config.DEBUG:
                msg = utils.colored_text(msg, utils.Colors.BRIGHT_YELLOW, True)
        except AttrDoesNotExistException:
            pass
        logger.warning(msg)


def create_conf_file(use_requests: bool = False, use_swagger: bool = False) -> Union[Exception, str]:
    """
    Creates a configuration file defining

    :param use_requests: Do you want to use requests, defaults to False
    :type use_requests: bool, optional
    :param use_swagger: Do you want to use swagger, defaults to False
    :type use_swagger: bool, optional
    :raises FileExistsError: Config file already exists
    :raises IOError: Config file creation failed.
    :return: Raises FileExistsError or IOError OR returns config_file_path
    :rtype: Union[Exception, str]
    """
    # Try using env value for config file, if not found use default
    CONFIG_FILE = os.getenv(CONFIGMAP_FILE_ENVIRONMENT, None)
    if not CONFIG_FILE:
        CONFIG_FILE = DEFAULT_CONFIGMAP_FILENAME
    # Prevent overwriting existing file
    if os.path.exists(CONFIG_FILE):
        raise FileExistsError("Config file already exists at '{}'".format(os.path.abspath(CONFIG_FILE)))
    # Create config dict
    config = {"pyms": {}}
    # add services
    if use_requests:
        if not config["pyms"].get("services", None):
            config["pyms"]["services"] = {}
        config["pyms"]["services"]["requests"] = {"data": ""}
    if use_swagger:
        if not config["pyms"].get("services", None):
            config["pyms"]["services"] = {}
        config["pyms"]["services"]["swagger"] = {"path": "", "file": "swagger.yaml"}
    # add Basic Flask config
    config["pyms"]["config"] = {
        "DEBUG": True,
        "TESTING": False,
        "APP_NAME": "Python Microservice",
        "APPLICATION_ROOT": "",
    }
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as config_file:
            config_file.write(yaml.dump(config, default_flow_style=False, default_style=None, sort_keys=False))
    except Exception as ex:
        raise ex
    return CONFIG_FILE
