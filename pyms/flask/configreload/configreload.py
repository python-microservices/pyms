from __future__ import unicode_literals, print_function, absolute_import, division

from flask import Blueprint

configreload_blueprint = Blueprint('configreload', __name__, static_url_path='/static')


@configreload_blueprint.route('/reload_config', methods=['GET'])
def reloadconfig():
    from pyms.flask.app import Microservice
    """Reread configuration from file.
    :return:
    """
    Microservice().reload_conf()
    return "OK"
