from __future__ import unicode_literals, print_function, absolute_import, division

from flask import Blueprint

healthcheck_blueprint = Blueprint('healthcheck', __name__, static_url_path='/static')


@healthcheck_blueprint.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Set a healtcheck to help other service to discover this microservice, like Kubernetes, AWS ELB, etc.
    :return:
    """
    return "OK"
