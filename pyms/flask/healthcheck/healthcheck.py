from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint

healthcheck_blueprint = Blueprint("healthcheck", __name__, static_url_path="/static")


@healthcheck_blueprint.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Set a healthcheck to help other service to discover this microservice, like Kubernetes, AWS ELB, etc.
    :return:
    """
    return "OK"
