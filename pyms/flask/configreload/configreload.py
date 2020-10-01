from __future__ import unicode_literals, print_function, absolute_import, division
from flask import Blueprint

configreload_blueprint = Blueprint('configreload', __name__, static_url_path='/static')


@configreload_blueprint.route('/reload_config', methods=['GET'])
def reloadconfig():
    """
    Reread configuration from file.
    :return:
    """
    # pylint: disable=import-outside-toplevel
    from pyms.flask.app import microservice
    microservice().reload_conf()
    return "OK"
