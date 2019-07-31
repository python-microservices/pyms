from pyms.flask.app.create_app import Microservice


def config(ms_class=Microservice, service="ms"):
    ms = ms_class(service=service, path=__file__)
    return ms.config