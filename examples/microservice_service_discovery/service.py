import json

import requests

from pyms.flask.services.service_discovery import ServiceDiscoveryBase


class ServiceDiscoveryConsulBasic(ServiceDiscoveryBase):
    def register_service(self, id_app, host, port, healtcheck_url, app_name):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "id": app_name + "-" + id_app,
            "name": app_name,
            "check": {"name": "ping check", "http": healtcheck_url, "interval": "30s", "status": "passing"},
        }
        response = requests.put(
            "http://{host}:{port}/v1/agent/service/register".format(host=host, port=port),
            data=json.dumps(data),
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.content)
