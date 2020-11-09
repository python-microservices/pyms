from typing import Dict


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances: Dict[type, type] = {}
    _singleton = True

    def __call__(cls, *args, **kwargs) -> type:
        if cls not in cls._instances or not cls._singleton:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]


class ReverseProxied:
    """
    Create a Proxy pattern https://microservices.io/patterns/apigateway.html.
    You can run the microservice A in your local machine in http://localhost:5000/my-endpoint/
    If you deploy your microservice, in some cases this microservice run behind a cluster, a gateway... and this
    gateway redirect traffic to the microservice with a specific path like yourdomian.com/my-ms-a/my-endpoint/.
    This class understand this path if the gateway send a specific header
    """

    def __init__(self, app):
        self.app = app

    @staticmethod
    def _extract_prefix(environ: dict) -> str:
        """
        Get Path from environment from:
        - Traefik with HTTP_X_SCRIPT_NAME https://docs.traefik.io/v2.0/middlewares/headers/
        - Nginx and Ingress with HTTP_X_SCRIPT_NAME https://www.nginx.com/resources/wiki/start/topics/examples/forwarded/
        - Apache with HTTP_X_SCRIPT_NAME https://stackoverflow.com/questions/55619013/proxy-and-rewrite-to-webapp
        - Zuul with  HTTP_X_FORWARDER_PREFIX https://cloud.spring.io/spring-cloud-netflix/multi/multi__router_and_filter_zuul.html
        :param environ:
        :return:
        """
        # Get path from Traefik, Nginx and Apache
        path = environ.get("HTTP_X_SCRIPT_NAME", "")
        if not path:
            # Get path from Zuul
            path = environ.get("HTTP_X_FORWARDED_PREFIX", "")
        if path and not path.startswith("/"):
            path = "/" + path
        return path

    def __call__(self, environ, start_response):
        script_name = self._extract_prefix(environ)
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name) :]  # noqa: E203

        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)
