import logging

from pyms.config.conf import get_conf
from pyms.constants import SERVICE_BASE, LOGGER_NAME
from pyms.utils.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


class DriverService:
    service = ""

    def __init__(self, service, *args, **kwargs):
        self.service = ".".join([service, self.service])
        self.config = get_conf(service=self.service, empty_init=True)

    def __getattr__(self, attr, *args, **kwargs):
        config_attribute = getattr(self.config, attr)
        return config_attribute if config_attribute is "" or config_attribute != {} else self.default_values.get(attr,
                                                                                                                 None)


class ServicesManager:
    service = SERVICE_BASE

    def __init__(self, service=None):
        self.service = (service if service else SERVICE_BASE)
        self.config = get_conf(service=self.service, empty_init=True)

    def get_services(self):
        return ((k, self.get_service(k)) for k in self.config.__dict__.keys() if k not in ['empty_init', ])

    def get_service(self, service, *args, **kwargs):
        service_object = import_from("pyms.flask.services.{}".format(service), "Service")
        logger.info("Init service {}".format(service))
        return service_object(service=self.service, *args, **kwargs)
