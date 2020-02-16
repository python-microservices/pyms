import os

import connexion
from connexion.resolver import RestyResolver

from pyms.flask.services.driver import DriverService
from pyms.utils import check_package_exists

SWAGGER_PATH = "swagger"
SWAGGER_FILE = "swagger.yaml"
SWAGGER_URL = "ui/"
PROJECT_DIR = "project"


class Service(DriverService):
    """The parameters you can add to your config are:
    * **path:** The relative or absolute route to your swagger yaml file. The default value is the current directory
    * **file:** The name of you swagger yaml file. The default value is `swagger.yaml`
    * **url:** The url where swagger run in your server. The default value is `/ui/`.
    * **project_dir:** Relative path of the project folder to automatic routing,
    see [this link for more info](https://github.com/zalando/connexion#automatic-routing). The default value is `project`
    """
    service = "swagger"
    default_values = {
        "path": SWAGGER_PATH,
        "file": SWAGGER_FILE,
        "url": SWAGGER_URL,
        "project_dir": PROJECT_DIR
    }

    def init_app(self, config, path):
        check_package_exists("connexion")
        app = connexion.App(__name__,
                            specification_dir=os.path.join(path, self.path),
                            resolver=RestyResolver(self.project_dir))
        app.add_api(
            self.file,
            arguments={'title': config.APP_NAME},
            base_path=config.APPLICATION_ROOT,
            options={"swagger_url": self.url}
        )
        # Invert the objects, instead connexion with a Flask object, a Flask object with
        application = app.app
        application.connexion_app = app
        return application
