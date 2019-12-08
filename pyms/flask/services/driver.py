import logging

from pyms.config import get_conf, ConfFile
from pyms.constants import SERVICE_BASE, LOGGER_NAME
from pyms.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


class DriverService:
    """All services must inherit from this class. This set the configuration. If we have got his config file:
    ```
    pyms:
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
    my-ms:
      DEBUG: true
      TESTING: true
    ```
    * `pyms` block is the default key to load in the pyms.flask.app.create_app.Microservice class.
        * `metrics`: is set as the service `pyms.metrics`
        * `swagger`: is set as the service `pyms.swagger`
        * `tracer`: is set as the service `pyms.tracer`
    """
    service = ""
    config = None

    def __init__(self, service, *args, **kwargs):
        self.service = ".".join([service, self.service])
        self.config = get_conf(service=self.service, empty_init=True, memoize=kwargs.get("memoize", True))

    def __getattr__(self, attr, *args, **kwargs):
        config_attribute = getattr(self.config, attr)
        return config_attribute if config_attribute == "" or config_attribute != {} else self.default_values.get(attr,
                                                                                                                 None)

    def exists_config(self):
        return self.config is not None and isinstance(self.config, ConfFile)


class ServicesManager:
    """This class works between `pyms.flask.create_app.Microservice` and `pyms.flask.services.[THESERVICE]`. Search
    for a file with the name you want to load, set the configuration and return a instance of the class you want
    """
    service = SERVICE_BASE

    def __init__(self, service=None):
        self.service = (service if service else SERVICE_BASE)
        self.config = get_conf(service=self.service, empty_init=True, memoize=False)

    def get_services(self, memoize):
        return ((k, self.get_service(k, memoize=memoize)) for k in self.config.__dict__.keys() if k not in ['empty_init', ])

    def get_service(self, service, *args, **kwargs):
        service_object = import_from("pyms.flask.services.{}".format(service), "Service")
        logger.debug("Init service {}".format(service))
        return service_object(service=self.service, *args, **kwargs)
