"""
Consulate: A client library for Consul

"""
import logging
from logging import NullHandler

from pyms.services_discovery.consulate.client import Consul
from pyms.services_discovery.consulate.exceptions import (ConsulateException,
                                                          ClientError,
                                                          ServerError,
                                                          ACLDisabled,
                                                          Forbidden,
                                                          NotFound,
                                                          LockFailure,
                                                          RequestError)

__version__ = '1.0.0'

# Prevent undesired log output to the root logger
logging.getLogger('consulate').addHandler(NullHandler())

__all__ = [
    __version__,
    Consul,
    ConsulateException,
    ClientError,
    ServerError,
    ACLDisabled,
    Forbidden,
    NotFound,
    LockFailure,
    RequestError
]
