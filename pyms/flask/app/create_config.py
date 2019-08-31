from pyms.flask.app.create_app import Microservice


def config():
    ms = Microservice()
    return ms.config
