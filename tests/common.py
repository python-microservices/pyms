import os
from pyms.flask.app import Microservice
from pyms.constants import CONFIGMAP_FILE_ENVIRONMENT, DEFAULT_CONFIGMAP_FILENAME

class MyMicroserviceNoSingleton(Microservice):
    _singleton = False


class MyMicroservice(Microservice):
    pass


def remove_conf_file():
    """
    Remove the YAML config file
    """
    CONFIG_FILE = os.getenv(CONFIGMAP_FILE_ENVIRONMENT, None)
    if not CONFIG_FILE:
        CONFIG_FILE = DEFAULT_CONFIGMAP_FILENAME
    # Dlete file, if exists
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
