"""Healthcheck
"""
from pyms.flask.healthcheck import healthcheck_blueprint


@healthcheck_blueprint.route('/healthcheck', methods=['GET'])
def healthcheck():
    return "OK"
