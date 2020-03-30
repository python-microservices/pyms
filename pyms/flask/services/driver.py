import logging
from typing import Text, Tuple

from pyms.config import ConfFile
from pyms.config.resource import ConfigResource
from pyms.constants import SERVICE_BASE, LOGGER_NAME
from pyms.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


def get_service_name(service_base=SERVICE_BASE, service=""):
    return ".".join([service_base, service])


class DriverService(ConfigResource):
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
    enabled = True

    def __init__(self, *args, **kwargs):
        self.config_resource = get_service_name(service=self.config_resource)
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr, *args, **kwargs):
        config_attribute = getattr(self.config, attr)
        return config_attribute if config_attribute == "" or config_attribute != {} else self.default_values.get(attr,
                                                                                                                 None)

    def is_enabled(self):
        return self.enabled

    def exists_config(self):
        return self.config is not None and isinstance(self.config, ConfFile)


class ServicesResource(ConfigResource):
    """This class works between `pyms.flask.create_app.Microservice` and `pyms.flask.services.[THESERVICE]`. Search
    for a file with the name you want to load, set the configuration and return a instance of the class you want
    """
    config_resource = SERVICE_BASE

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
