from __future__ import unicode_literals, print_function, absolute_import, division
from flask import Blueprint
from flask import current_app

configreload_blueprint = Blueprint('configreload', __name__, static_url_path='/static')


@configreload_blueprint.route('/reload-config', methods=['POST'])
def reloadconfig():
    """
    Reread configuration from file.
    :return:
    """
    current_app.ms.reload_conf()
    return "OK"
