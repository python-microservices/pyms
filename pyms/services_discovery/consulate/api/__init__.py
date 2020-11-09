"""
Consul API Endpoints

"""
from pyms.services_discovery.consulate.api.acl import ACL
from pyms.services_discovery.consulate.api.agent import Agent
from pyms.services_discovery.consulate.api.catalog import Catalog
from pyms.services_discovery.consulate.api.event import Event
from pyms.services_discovery.consulate.api.health import Health
from pyms.services_discovery.consulate.api.coordinate import Coordinate
from pyms.services_discovery.consulate.api.kv import KV
from pyms.services_discovery.consulate.api.lock import Lock
from pyms.services_discovery.consulate.api.session import Session
from pyms.services_discovery.consulate.api.status import Status
from pyms.services_discovery.consulate.api.base import Response

__all__ = ["ACL", "Agent", "Catalog", "Event", "Health", "KV", "Lock", "Session", "Status", "Response"]
