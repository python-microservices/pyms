"""Creación del tracer para progagar las trazas entre micros y servicios
"""
from jaeger_client import Config


def init_jaeger_tracer():
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