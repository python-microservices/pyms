from pyms.flask.app import config

GLOBAL_VARIABLE = config().request_variable_test
GLOBAL_VARIABLE2 = config().MyVar


def example():
    return {
        "GLOBAL_VARIABLE": GLOBAL_VARIABLE,
        "GLOBAL_VARIABLE2": GLOBAL_VARIABLE2,
        "test1": config().test1,
        "test2": config().test2
    }
