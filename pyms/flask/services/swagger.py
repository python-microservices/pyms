from pyms.flask.services.driver import DriverService

SWAGGER_PATH = "swagger"
SWAGGER_FILE = "swagger.yaml"


class Service(DriverService):
    service = "swagger"
    default_values = {
        "path": SWAGGER_PATH,
        "file": SWAGGER_FILE
    }
