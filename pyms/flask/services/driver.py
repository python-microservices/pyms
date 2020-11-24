import logging
from typing import Iterator, Text, Tuple

from pyms.config import ConfFile
from pyms.config.resource import ConfigResource
from pyms.constants import LOGGER_NAME, SERVICE_BASE
from pyms.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


def get_service_name(service_base: str = SERVICE_BASE, service: str = "") -> str:
    return ".".join([service_base, service])


class DriverService(ConfigResource):
    """All services must inherit from this class. This set the configuration. If we have got his config file:
    See these docs:
    * https://python-microservices.github.io/configuration/
    * https://python-microservices.github.io/services/
    """

    enabled = True

    init_action = False

    def __init__(self, *args, **kwargs):
        self.config_resource = get_service_name(service=self.config_resource)
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr, *args, **kwargs):
        config_attribute = getattr(self.config, attr)
        return (
            config_attribute
            if config_attribute == "" or config_attribute != {}
            else self.default_values.get(attr, None)
        )

    def is_enabled(self) -> bool:
        return self.enabled

    def exists_config(self) -> bool:
        return self.config is not None and isinstance(self.config, ConfFile)


class ServicesResource(ConfigResource):
    """This class works between `pyms.flask.create_app.Microservice` and `pyms.flask.services.[THESERVICE]`. Search
    for a file with the name you want to load, set the configuration and return a instance of the class you want
    See these docs:
    * https://python-microservices.github.io/configuration/
    * https://python-microservices.github.io/services/
    """

    config_resource = SERVICE_BASE

    def get_services(self) -> Iterator[Tuple[Text, DriverService]]:
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
