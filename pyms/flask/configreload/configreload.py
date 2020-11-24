from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, current_app

configreload_blueprint = Blueprint("configreload", __name__, static_url_path="/static")


@configreload_blueprint.route("/reload-config", methods=["POST"])
def reloadconfig():
    """
    Reread configuration from file.
    :return:
    """
    current_app.ms.reload_conf()
    return "OK"
