import logging

try:
    import opentracing
except ModuleNotFoundError:  # pragma: no cover
    opentracing = None
try:
    from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
except ModuleNotFoundError:  # pragma: no cover
    PrometheusMetricsFactory = None
try:
    from opentracing_instrumentation import get_current_span
except ModuleNotFoundError:  # pragma: no cover
    get_current_span = None

from flask import current_app, request, has_request_context

from pyms.config.conf import get_conf
from pyms.constants import LOGGER_NAME
from pyms.flask.services.driver import DriverService
from pyms.utils import check_package_exists, import_package, import_from
from pyms.utils.utils import get_service_name

logger = logging.getLogger(LOGGER_NAME)

JAEGER_CLIENT = "jaeger"
LIGHT_CLIENT = "lightstep"

DEFAULT_CLIENT = JAEGER_CLIENT


def inject_span_in_headers(headers):
    if has_request_context():
        # FLASK https://github.com/opentracing-contrib/python-flask
        tracer = current_app.tracer if getattr(current_app, "tracer") else None
        # Add traces
        span = None
        current_app.app_context()
        if tracer:
            span = tracer.get_span(request=request)
            if not span:  # pragma: no cover
                span = get_current_span()
                if not span:
                    span = tracer.tracer.start_span()
        context = span.context if span else None
        tracer.tracer.inject(context, opentracing.Format.HTTP_HEADERS, headers)
    return headers


class Service(DriverService):
    """
    Add trace to all executions with [opentracing](https://github.com/opentracing-contrib/python-flask).
    All default values keys are created as class attributes in `DriverService`
    """
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
        metrics_config = get_conf(service=get_service_name(service="metrics"), empty_init=True)
        metrics = ""
        if metrics_config:
            service_name = self.component_name.lower().replace("-", "_").replace(" ", "_")
            metrics = PrometheusMetricsFactory(service_name_label=service_name)
        config = Config(
            config={
                **{
                    'sampler': {
                        'type': 'const',
                        'param': 1,
                    },
                    'propagation': 'b3',
                    'logging': True
                },
                **host
            }, service_name=self.component_name,
            metrics_factory=metrics,
            validate=True
        )
        return config.initialize_tracer()

    def init_lightstep_tracer(self):
        check_package_exists("lightstep")
        lightstep = import_package("lightstep")
        return lightstep.Tracer(component_name=self.component_name)
