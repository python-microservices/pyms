import logging
from typing import Text, Tuple

from pyms.config import get_conf, ConfFile
from pyms.constants import SERVICE_BASE, LOGGER_NAME
from pyms.utils import import_from
from pyms.utils.utils import get_service_name

logger = logging.getLogger(LOGGER_NAME)


class DriverService:
    """All services must inherit from this class. This set the configuration. If we have got his config file:
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
    * `pyms.services` block is the default key to load in the pyms.flask.app.create_app.Microservice class.
        * `metrics`: is set as the service `pyms.services.metrics`
        * `swagger`: is set as the service `pyms.services.swagger`
        * `tracer`: is set as the service `pyms.services.tracer`
    """
    service = ""
    config = None
    enabled = True

    def __init__(self, *args, **kwargs):
        self.service = get_service_name(service=self.service)
        self.config = get_conf(service=self.service, empty_init=True)

    def __getattr__(self, attr, *args, **kwargs):
        config_attribute = getattr(self.config, attr)
        return config_attribute if config_attribute == "" or config_attribute != {} else self.default_values.get(attr,
                                                                                                                 None)

    def is_enabled(self):
        return self.enabled

    def exists_config(self):
        return self.config is not None and isinstance(self.config, ConfFile)


class ServicesManager:
    """This class works between `pyms.flask.create_app.Microservice` and `pyms.flask.services.[THESERVICE]`. Search
    for a file with the name you want to load, set the configuration and return a instance of the class you want
    """
    service = SERVICE_BASE

    def __init__(self):
        self.config = get_conf(service=self.service, empty_init=True, uppercase=False)

    def get_services(self) -> Tuple[Text, DriverService]:
        for k in self.config.__dict__.keys():
            if k.islower() and not k.startswith("_"):
                service = self.get_service(k)
                if service.is_enabled():
                    yield k, service

    @staticmethod
    def get_service(service: Text, *args, **kwargs) -> DriverService:
        service_object = import_from("pyms.flask.services.{}".format(service), "Service")
        logger.debug("Init service {}".format(service))
        return service_object(*args, **kwargs)
