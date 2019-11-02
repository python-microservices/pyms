import logging

from pyms.constants import LOGGER_NAME

from pyms.flask.services.driver import DriverService

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
        from jaeger_client import Config

        """This scaffold is configured whith `Jeager <https://github.com/jaegertracing/jaeger>`_ but you can use
        one of the `opentracing tracers <http://opentracing.io/documentation/pages/supported-tracers.html>`_
        :param service_name: the name of your application to register in the tracer
        :return: opentracing.Tracer
        """
        host = {}
        if self.host:
            host = {
                'local_agent': {
                    'reporting_host': self.host,
                    'reporting_port': '5775',
                }
            }

        config = Config(config={
            **{
                'propagation': 'b3',
                'logging': True
            },
            **host
        }, service_name=self.component_name)
        return config.initialize_tracer()

    def init_lightstep_tracer(self):
        import lightstep
        return lightstep.Tracer(component_name=self.component_name)
