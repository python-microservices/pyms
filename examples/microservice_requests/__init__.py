import os

from pyms.flask.app import Microservice

os.environ["CONFIGMAP_FILE"] = "config.yml"
ms = Microservice(service="my-ms", path=__file__)