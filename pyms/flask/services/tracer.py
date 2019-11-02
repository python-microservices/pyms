from flask_opentracing import FlaskTracing

from pyms.flask.services.driver import DriverService

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

        return opentracing_tracer

    @staticmethod
    def init_jaeger_tracer():
        from jaeger_client import Config

        """This scaffold is configured whith `Jeager <https://github.com/jaegertracing/jaeger>`_ but you can use
        one of the `opentracing tracers <http://opentracing.io/documentation/pages/supported-tracers.html>`_
        :param service_name: the name of your application to register in the tracer
        :return: opentracing.Tracer
        """
        config = Config(config={
            'propagation': 'b3',
            'logging': True,
        }, service_name="data-connection")
        return config.initialize_tracer()

    @staticmethod
    def init_lightstep_tracer():
        import lightstep
        return lightstep.Tracer(component_name="ms")
