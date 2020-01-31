from pyms.flask.app.create_app import Microservice


def config():
    """The behavior of this function is to access to the configuration outer the scope of flask context, to prevent to
     raise a `'working outside of application context`
    **IMPORTANT:** If you use this method to get configuration out of context, you must set the `CONFIGMAP_SERVICE` or
    set the default key `ms` for your configuration block in your config.yml
    :return:
    """
    ms = Microservice()
    return ms.config
