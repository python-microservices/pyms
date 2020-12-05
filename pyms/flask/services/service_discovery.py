import logging

try:
    import consulate
except ModuleNotFoundError:  # pragma: no cover
    consulate = None

from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService
from pyms.utils.utils import import_class

logger = logging.getLogger(LOGGER_NAME)

CONSUL_SERVICE_DISCOVERY = "consul"

DEFAULT_SERVICE_DISCOVERY = CONSUL_SERVICE_DISCOVERY


class ServiceDiscoveryBase:
    client = None

    def __init__(self, config):
        pass

    def register_service(self, *args, **kwargs):
        pass


class ServiceDiscoveryConsul(ServiceDiscoveryBase):
    def __init__(self, config):
        super().__init__(config)
        self.client = consulate.Consul(
            host=config.host, port=config.port, token=config.token, scheme=config.scheme, adapter=config.adapter
        )

    def register_service(self, *args, **kwargs):
        self.client.agent.check.register(
            kwargs["app_name"], http=kwargs["healtcheck_url"], interval=kwargs.get("interval", "10s")
        )


class Service(DriverService):
    config_resource = "service_discovery"
    default_values = {
        "service": DEFAULT_SERVICE_DISCOVERY,
        "host": "localhost",
        "scheme": "http",
        "port": 8500,
        "healtcheck_url": "http://127.0.0.1.nip.io:5000/healthcheck",
        "interval": "10s",
        "autoregister": False,
    }

    def init_action(self, microservice_instance):
        if self.autoregister:
            app_name = microservice_instance.application.config["APP_NAME"]
            self._client.register_service(healtcheck_url=self.healtcheck_url, app_name=app_name, interval=self.interval)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = self.get_client()
        self.client = self._client.client

    def get_client(self) -> ServiceDiscoveryBase:
        if self.service == CONSUL_SERVICE_DISCOVERY:
            client = ServiceDiscoveryConsul(self)
        else:
            client = import_class(self.service)(self)

        logger.debug("Init %s as service discovery", client)
        return client
