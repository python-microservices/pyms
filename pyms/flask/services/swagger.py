import os

import connexion
from connexion.resolver import RestyResolver

from pyms.exceptions import AttrDoesNotExistException
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
      see [this link for more info](https://github.com/zalando/connexion#automatic-routing).
      The default value is `project`

    All default values keys are created as class attributes in `DriverService`
    """
    service = "swagger"
    default_values = {
        "path": SWAGGER_PATH,
        "file": SWAGGER_FILE,
        "url": SWAGGER_URL,
        "project_dir": PROJECT_DIR
    }

    @staticmethod
    def _get_application_root(config):
        try:
            application_root = config.APPLICATION_ROOT
        except AttrDoesNotExistException:
            application_root = "/"
        return application_root

    def init_app(self, config, path):
        """
        Initialize Connexion App. See more info in [Connexion Github](https://github.com/zalando/connexion)
        :param config: The Flask configuration defined in the config.yaml:
        ```yaml
        pyms:
          services:
            requests: true
            swagger:
              path: ""
              file: "swagger.yaml"
          config: <!--
            DEBUG: true
            TESTING: false
            APP_NAME: "Python Microservice"
            APPLICATION_ROOT: ""
        ```
        :param path: The current path where is instantiated Microservice class:
        ```
        Microservice(path=__file__)
                     ^^^^--- This param
        ```
        :return: Flask
        """
        check_package_exists("connexion")
        specification_dir = self.path
        application_root = self._get_application_root(config)
        if not os.path.isabs(self.path):
            specification_dir = os.path.join(path, self.path)

        app = connexion.App(__name__,
                            specification_dir=specification_dir,
                            resolver=RestyResolver(self.project_dir))

        params = {
            "specification": self.file,
            "arguments": {'title': config.APP_NAME},
            "base_path": application_root,
            "options": {"swagger_url": self.url},
        }

        # Fix Connexion issue https://github.com/zalando/connexion/issues/1135
        if application_root == "/":
            params["base_path"] = ""

        app.add_api(**params)
        # Invert the objects, instead connexion with a Flask object, a Flask object with
        application = app.app
        application.connexion_app = app
        return application
