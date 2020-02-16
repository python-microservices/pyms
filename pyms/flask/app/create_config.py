from pyms.flask.app.create_app import Microservice


def config():
    """The behavior of this function is to access to the configuration outer the scope of flask context, to prevent to
     raise a `'working outside of application context`
    :return:
    """
    ms = Microservice()
    return ms.config
