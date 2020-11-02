import json
import logging
import uuid

import requests
from requests.exceptions import RequestException
from pyms.constants import LOGGER_NAME
from pyms.exceptions import ServiceDiscoveryConnectionException
from pyms.flask.services.driver import DriverService

logger = logging.getLogger(LOGGER_NAME)

CONSUL_SERVICE_DISCOVERY = "consul"

DEFAULT_SERVICE_DISCOVERY = CONSUL_SERVICE_DISCOVERY


class ServiceDiscoveryBase:
    def register_service(self, id_app, host, port, healtcheck_url, app_name):
        pass


class ServiceDiscoveryConsul(ServiceDiscoveryBase):
    def register_service(self, id_app, host, port, healtcheck_url, app_name):
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
            "id": app_name + "-" + id_app,
            "name": app_name,
            "port": port,
            "check": {
                "name": "ping check",
                "http": healtcheck_url,
                "interval": "30s",
                "status": "passing"
            }
        }
        error = False
        msg_error = "Failed to establish a new connection"
        try:
            response = requests.put("{host}/v1/agent/service/register".format(host=host), data=json.dumps(data),
                                    headers=headers)
            if response.status_code != 200:
                msg_error = response.content
                error = True
        except RequestException:
            error = True

        if error:
            raise ServiceDiscoveryConnectionException("Host %s raise an error: %s" % (host, msg_error))


class Service(DriverService):
    id_app = str(uuid.uuid1())
    config_resource = "service_discovery"
    default_values = {
        "client": DEFAULT_SERVICE_DISCOVERY,
        "host": "http://localhost:8500",
        "port": 5000,
        "healtcheck_url": "http://127.0.0.1.nip.io:5000/healthcheck",
    }

    def init_action(self, microservice_instance):
        self.client.register_service(
            id_app=self.id_app,
            host=self.host,
            healtcheck_url=self.healtcheck_url,
            port=self.port,
            app_name=microservice_instance.application.config["APP_NAME"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.get_client()

    def get_client(self) -> ServiceDiscoveryBase:
        client = False
        if self.config.client == CONSUL_SERVICE_DISCOVERY:
            client = ServiceDiscoveryConsul()

        logger.debug("Init %s as service discovery", client)
        return client
