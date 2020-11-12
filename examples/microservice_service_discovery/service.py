import json
import uuid

import requests

from pyms.flask.services.service_discovery import ServiceDiscoveryBase


class ServiceDiscoveryConsulBasic(ServiceDiscoveryBase):
    id_app = str(uuid.uuid1())

    def __init__(self, config):
        super().__init__(config)
        self.host = config.host
        self.port = config.port

    def register_service(self, *args, **kwargs):
        app_name = kwargs["app_name"]
        healtcheck_url = kwargs["healtcheck_url"]
        interval = kwargs["interval"]
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "id": app_name + "-" + self.id_app,
            "name": app_name,
            "check": {"name": "ping check", "http": healtcheck_url, "interval": interval, "status": "passing"},
        }
        response = requests.put(
            "http://{host}:{port}/v1/agent/service/register".format(host=self.host, port=self.port),
            data=json.dumps(data),
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.content)
