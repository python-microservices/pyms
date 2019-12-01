import logging

from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService
from pyms.utils import check_package_exists, import_package, import_from
from pyms.config.conf import get_conf

logger = logging.getLogger(LOGGER_NAME)

JAEGER_CLIENT = "jaeger"
LIGHT_CLIENT = "lightstep"

DEFAULT_CLIENT = JAEGER_CLIENT


class Service(DriverService):
    service = "tracer"
    default_values = {
        "client": DEFAULT_CLIENT,
    }

    def get_client(self):
        opentracing_tracer = False
        if self.config.client == JAEGER_CLIENT:
            opentracing_tracer = self.init_jaeger_tracer()
        elif self.config.client == LIGHT_CLIENT:
            opentracing_tracer = self.init_lightstep_tracer()

        logger.debug("Init %s as tracer client", opentracing_tracer)
        return opentracing_tracer

    def init_jaeger_tracer(self):
        """This scaffold is configured whith `Jeager <https://github.com/jaegertracing/jaeger>`_ but you can use
        one of the `opentracing tracers <http://opentracing.io/documentation/pages/supported-tracers.html>`_
        :param service_name: the name of your application to register in the tracer
        :return: opentracing.Tracer
        """
        check_package_exists("jaeger_client")
        Config = import_from("jaeger_client", "Config")
        host = {}
        if self.host:
            host = {
                'local_agent': {
                    'reporting_host': self.host
                }
            }
        metrics_config = get_conf(service="pyms.metrics", empty_init=True, memoize=False)
        metrics = ""
        if metrics_config:
            service_name = self.component_name.lower().replace("-", "_").replace(" ", "_")
            metrics = PrometheusMetricsFactory()
        config = Config(config={
            **{'sampler': {
                'type': 'const',
                'param': 1,
            },
                'propagation': 'b3',
                'logging': True
            },
            **host
        }, service_name=self.component_name,
            metrics_factory=metrics,
            validate=True)
        return config.initialize_tracer()

    def init_lightstep_tracer(self):
        check_package_exists("lightstep")
        lightstep = import_package("lightstep")
        return lightstep.Tracer(component_name=self.component_name)
