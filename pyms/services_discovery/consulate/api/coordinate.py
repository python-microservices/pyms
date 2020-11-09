"""
Consul Coordinate Endpoint Access

"""
from math import sqrt

from pyms.services_discovery.consulate.api import base


class Coordinate(base.Endpoint):
    """Used to query node coordinates."""

    def node(self, node_id):
        """Return coordinates for the given node.

        :param str node_id: The node ID
        :rtype: dict

        """
        return self._get(["node", node_id])

    def nodes(self):
        """Return coordinates for the current datacenter.

        :rtype: list

        """
        return self._get_list(["nodes"])

    @staticmethod
    def rtt(src, dst):
        """Calculated RTT between two node coordinates.
        :param src:
        :param dst:
        :return:
        """

        if not isinstance(src, (dict)):
            raise ValueError("coordinate object must be a dictionary")
        if not isinstance(dst, (dict)):
            raise ValueError("coordinate object must be a dictionary")
        if "Coord" not in src:
            raise ValueError("coordinate object has no Coord key")
        if "Coord" not in dst:
            raise ValueError("coordinate object has no Coord key")

        src_coord = src["Coord"]
        dst_coord = dst["Coord"]

        if len(src_coord.get("Vec")) != len(dst_coord.get("Vec")):
            raise ValueError("coordinate objects are not compatible due to different length")

        sumsq = 0.0
        for i in range(len(src_coord.get("Vec"))):
            diff = src_coord.get("Vec")[i] - dst_coord.get("Vec")[i]
            sumsq += diff * diff

        rtt = sqrt(sumsq) + src_coord.get("Height") + dst_coord.get("Height")
        adjusted = rtt + src_coord.get("Adjustment") + dst_coord.get("Adjustment")
        if adjusted > 0.0:
            rtt = adjusted

        return rtt * 1000
