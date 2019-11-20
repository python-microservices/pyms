from pyms.config.confile import ConfFile
from pyms.exceptions import ServiceDoesNotExistException


__service_configs = {}


def get_conf(*args, **kwargs):
    service = kwargs.pop('service', None)
    if not service:
        raise ServiceDoesNotExistException("Service not defined")
    if service not in __service_configs:
        __service_configs[service] = ConfFile(*args, **kwargs)
    return getattr(__service_configs[service], service)
