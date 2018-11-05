"""Init file
"""
from __future__ import unicode_literals, print_function, absolute_import, division

from flask import Blueprint

healthcheck_blueprint = Blueprint('healthcheck', __name__, static_url_path='/static')

from pyms.flask.healthcheck import healthcheck
