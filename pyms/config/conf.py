from pyms.config.confile import ConfFile
from pyms.exceptions import ServiceDoesNotExistException


class Config:
    service = None
    _config = False

    def __init__(self):
        pass

    def config(self, *args, **kwargs):
        """Set the configuration, if our yaml file is like:
        myservice:
          myservice1:
           myvar1
        and we want to get the configuration of service1, our self.service will be "myservice.myservice1"
        """
        if not self._config:
            self._config = ConfFile(*args, **kwargs)
        if not self.service:
            raise ServiceDoesNotExistException("Service not defined")
        return getattr(self._config, self.service)


def get_conf(service=None, *args, **kwargs):
    config = Config()
    config.service = service
    return config.config(*args, **kwargs)
