from pyms.exceptions import AttrDoesNotExistException

from pyms.config.conf import get_conf
from pyms.constants import SWAGGER_PATH, SWAGGER_FILE


class Swagger:
    service = "swagger"

    def __init__(self):
        self.config = get_conf(service=self.service, empty_init=True)

    @property
    def path(self):
        path = self.config.path
        return path if path else SWAGGER_PATH

    @property
    def file(self):
        swagger_file = self.config.file
        return swagger_file if swagger_file else SWAGGER_FILE
