import logging
import os
from typing import List, Optional

from flask import Flask

from pyms.config.conf import validate_conf
from pyms.config.resource import ConfigResource
from pyms.constants import CONFIG_BASE, LOGGER_NAME
from pyms.crypt.driver import CryptResource
from pyms.flask.app.utils import ReverseProxied, SingletonMeta
from pyms.flask.configreload import configreload_blueprint
from pyms.flask.healthcheck import healthcheck_blueprint
from pyms.flask.services.driver import DriverService, ServicesResource
from pyms.logger import CustomJsonFormatter
from pyms.utils import check_package_exists

logger = logging.getLogger(LOGGER_NAME)


class Microservice(ConfigResource, metaclass=SingletonMeta):
    """The class Microservice is the core of all microservices built with PyMS.
    See this docs: https://python-microservices.github.io/ms_class/
    """

    config_resource = CONFIG_BASE
    services: List[str] = []
    application = Flask
    swagger: Optional[DriverService] = None
    request: Optional[DriverService] = None
    tracer: Optional[DriverService] = None
    metrics: Optional[DriverService] = None
    _singleton = True

    def __init__(self, *args, **kwargs):
        """
        You can get the relative path from the current directory with `__file__` in path param. The path must be
        the folder where PyMS search for default config file, default swagger definition and encrypt key.
        :param args:
        :param kwargs: "path", optional, the current directory where `Microservice` class is instanciated
        """
        path = kwargs.pop("path") if kwargs.get("path") else None
        self.path = os.path.abspath("")
        if path:
            self.path = os.path.dirname(os.path.abspath(path))

        validate_conf()
        self.init_crypt(path=self.path, *args, **kwargs)
        super().__init__(path=self.path, crypt=self.crypt, *args, **kwargs)
        self.init_services()

    def init_services(self) -> None:
        """
        Set the Attributes of all service defined in config.yml and exists in `pyms.flask.service` module
        :return: None
        """
        services_resources = ServicesResource()
        for service_name, service in services_resources.get_services():
            if service_name not in self.services or not getattr(self, service_name, False):
                self.services.append(service_name)
                setattr(self, service_name, service)

    def init_services_actions(self):
        for service_name in self.services:
            srv_action = getattr(getattr(self, service_name), "init_action")
            if srv_action:
                srv_action(self)

    def init_crypt(self, *args, **kwargs) -> None:
        """
        Set the Attributes of all service defined in config.yml and exists in `pyms.flask.service` module
        :return: None
        """
        crypt_object = CryptResource(*args, **kwargs)
        self.crypt = crypt_object

    def delete_services(self) -> None:
        """
        Set the Attributes of all service defined in config.yml and exists in `pyms.flask.service` module
        :return: None
        """
        for service_name in self.services:
            try:
                delattr(self, service_name)
            except AttributeError:
                pass

    def init_libs(self) -> Flask:
        """This function exists to override if you need to set more libs such as SQLAlchemy, CORs, and any else
        library needs to be init over flask, like the usual pattern [MYLIB].init_app(app)
        :return:
        """
        return self.application

    def init_logger(self) -> None:
        """
        Set a logger and return in JSON format.
        :return:
        """
        self.application.logger = logger
        os.environ["WERKZEUG_RUN_MAIN"] = "true"

        formatter = CustomJsonFormatter()
        formatter.add_service_name(self.application.config["APP_NAME"])
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)

        self.application.logger.addHandler(log_handler)

        self.application.logger.propagate = False

        if self.application.config["DEBUG"]:
            self.application.logger.setLevel(logging.DEBUG)
        else:  # pragma: no cover
            self.application.logger.setLevel(logging.INFO)

    def init_app(self) -> Flask:
        """Set attribute in flask `swagger`. See in `pyms.flask.services.swagger` how it works. If not set,
        run a "normal" Flask app.
        :return: None
        """
        if self.swagger:
            application = self.swagger.init_app(config=self.config.to_flask(), path=self.path)
        else:
            check_package_exists("flask")
            application = Flask(
                __name__,
                static_folder=os.path.join(self.path, "static"),
                template_folder=os.path.join(self.path, "templates"),
            )

        application.root_path = self.path

        # Fix connexion issue https://github.com/zalando/connexion/issues/527
        application.wsgi_app = ReverseProxied(application.wsgi_app)

        return application

    def reload_conf(self):
        self.delete_services()
        self.config.reload()
        self.services = []
        self.init_services()
        self.crypt.config.reload()
        self.create_app()

    def create_app(self) -> Flask:
        """Initialize the Flask app, register blueprints and initialize
        all libraries like Swagger, database,
        the trace system...
        return the app and the database objects.
        :return:
        """
        self.application = self.init_app()
        self.application.config.from_object(self.config.to_flask())
        self.application.ms = self

        # Initialize Blueprints
        self.application.register_blueprint(healthcheck_blueprint)
        self.application.register_blueprint(configreload_blueprint)

        self.init_libs()
        self.add_error_handlers()
        self.init_logger()

        self.init_services_actions()

        logger.debug("Started app with PyMS and this services: {}".format(self.services))

        return self.application

    def add_error_handlers(self) -> None:
        """Subclasses will override this method in order to add specific error handlers. This should be done with
        calls to add_error_handler method.
        """
        pass

    def add_error_handler(self, code_or_exception, handler) -> None:
        """Add custom handler for an error code or exception in the connexion app.

        :param code_or_exception: HTTP error code or exception
        :param handler: callback for error handler
        """
        self.application.connexion_app.add_error_handler(code_or_exception, handler)
