from __future__ import unicode_literals, print_function, absolute_import, division
from flask import Blueprint

from pyms.flask.app.utils import microservice

configreload_blueprint = Blueprint('configreload', __name__, static_url_path='/static')


@configreload_blueprint.route('/reload_config', methods=['GET'])
def reloadconfig():
    """Reread configuration from file.
    :return:
    """
    microservice().reload_conf()
    return "OK"
