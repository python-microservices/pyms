import logging
import uuid

try:
    import consulate
except ModuleNotFoundError:  # pragma: no cover
    consulate = None

from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService
from pyms.utils import import_from

logger = logging.getLogger(LOGGER_NAME)

CONSUL_SERVICE_DISCOVERY = "consul"

DEFAULT_SERVICE_DISCOVERY = CONSUL_SERVICE_DISCOVERY


class ServiceDiscoveryBase:
    client = None

    def register_service(self, *args, **kwargs):
        pass


class ServiceDiscoveryConsul(ServiceDiscoveryBase):
    def __init__(self, config):
        self.client = consulate.Consul(
            host=config.host, port=config.port, token=config.token, scheme=config.scheme, adapter=config.adapter
        )

    def register_service(self, *args, **kwargs):
        self.client.agent.check.register(
            kwargs["app_name"], http=kwargs["healtcheck_url"], interval=kwargs.get("interval", "10s")
        )


class Service(DriverService):
    id_app = str(uuid.uuid1())
    config_resource = "service_discovery"
    default_values = {
        "service": DEFAULT_SERVICE_DISCOVERY,
        "host": "localhost",
        "scheme": "http",
        "port": 8500,
        "healtcheck_url": "http://127.0.0.1.nip.io:5000/healthcheck",
        "autoregister": False,
    }

    def init_action(self, microservice_instance):
        if self.autoregister:
            app_name = microservice_instance.application.config["APP_NAME"]
            self._client.register_service(healtcheck_url=self.healtcheck_url, app_name=app_name)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = self.get_client()
        self.client = self._client.client

    def get_client(self) -> ServiceDiscoveryBase:
        if self.service == CONSUL_SERVICE_DISCOVERY:
            client = ServiceDiscoveryConsul(self)
        else:
            service_paths = self.service.split(".")
            package = ".".join(service_paths[:-1])
            client = import_from(package, service_paths[-1])()

        logger.debug("Init %s as service discovery", client)
        return client
