import logging
import os

from pyms.config.confile import ConfFile
from pyms.constants import PYMS_CONFIG_WHITELIST_KEYWORDS, CONFIGMAP_FILE_ENVIRONMENT_LEGACY, \
    CONFIGMAP_FILE_ENVIRONMENT, CRYPT_FILE_KEY_ENVIRONMENT, CRYPT_FILE_KEY_ENVIRONMENT_LEGACY, LOGGER_NAME
from pyms.exceptions import ServiceDoesNotExistException, ConfigErrorException, AttrDoesNotExistException
from pyms.utils import utils

logger = logging.getLogger(LOGGER_NAME)


def get_conf(*args, **kwargs):
    """
    Returns an object with a set of attributes retrieved from the configuration file. Each subblock is a append of the
    parent and this name, in example of the next yaml, tracer will be `pyms.tracer`. If we have got his config file:
    ```
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
        TESTING: true
    ```
    * `pyms.services`: block is the default key to load in the pyms.flask.app.create_app.Microservice class.
        * `metrics`: is set as the service `pyms.metrics`
        * `swagger`: is set as the service `pyms.swagger`
        * `tracer`: is set as the service `pyms.tracer`
    * `pyms.config`: This block is the default flask block config
    :param args:
    :param kwargs:

    :return:
    """
    service = kwargs.pop('service', None)
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
        raise ConfigErrorException("""Config file must start with `pyms` keyword, for example:
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
        TESTING: true""")
    try:
        config.pyms.config
    except AttrDoesNotExistException:
        is_config_ok = False
    if not is_config_ok:
        raise ConfigErrorException("""`pyms` block must contain a `config` keyword in your Config file, for example:
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
        TESTING: true""")
    wrong_keywords = [i for i in config.pyms if i not in PYMS_CONFIG_WHITELIST_KEYWORDS]
    if len(wrong_keywords) > 0:
        raise ConfigErrorException("""{} isn`t a valid keyword for pyms block, for example:
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
            TESTING: true""".format(wrong_keywords))

    # TODO Remove temporally deprecated warnings on future versions
    __verify_deprecated_env_variables(config)


def __verify_deprecated_env_variables(config):
    env_var_duplicated = "IMPORTANT: If you are using \"{}\" environment variable, \"{}\" value will be ignored."
    env_var_deprecated = "IMPORTANT: \"{}\" environment variable is deprecated on this version, use \"{}\" instead."

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
