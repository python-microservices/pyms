import os
from pathlib import Path
from typing import Dict, Any

import connexion
from connexion.resolver import RestyResolver

try:
    import prance
    from prance.util import formats, fs
except ModuleNotFoundError:  # pragma: no cover
    prance = None

from pyms.exceptions import AttrDoesNotExistException
from pyms.flask.services.driver import DriverService
from pyms.utils import check_package_exists

SWAGGER_PATH = "swagger"
SWAGGER_FILE = "swagger.yaml"
SWAGGER_URL = "ui/"
PROJECT_DIR = "project"


def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    """
    Get bundled specs
    :param main_file: Swagger file path
    :return:
    """
    parser = prance.ResolvingParser(str(main_file.absolute()),
                                    lazy=True, backend='openapi-spec-validator')
    parser.parse()
    return parser.specification


def merge_swagger_file(main_file: str):
    """
    Generate swagger into a single file
    :param main_file: Swagger file path
    :return:
    """
    input_file = Path(main_file)
    output_file = Path(input_file.parent, 'swagger-complete.yaml')

    contents = formats.serialize_spec(
        specs=get_bundled_specs(input_file),
        filename=output_file,
    )
    fs.write_file(filename=output_file,
                  contents=contents,
                  encoding='utf-8')


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
    config_resource = "swagger"
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
            "specification": get_bundled_specs(
                Path(os.path.join(specification_dir, self.file))) if prance else self.file,
            "arguments": {'title': config.APP_NAME},
            "base_path": application_root,
            "options": {"swagger_url": self.url},
        }

        # Fix Connexion issue https://github.com/zalando/connexion/issues/1135
        if application_root == "/":
            del params["base_path"]

        app.add_api(**params)
        # Invert the objects, instead connexion with a Flask object, a Flask object with
        application = app.app
        application.connexion_app = app
        return application
