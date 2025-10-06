import math
from typing import Dict, Optional
from container import Container

class Port:
    def __init__(self, latitude: float = 0.0, longitude: float = 0.0):
        cls = type(self)
        if not hasattr(cls, "_id_counter"):
            cls._id_counter = 0
        self.ID = cls._id_counter
        cls._id_counter += 1

        self.latitude = latitude
        self.longitude = longitude

        self.containers: Dict[int, Container] = {}
        self.history: Dict[int, "Ship"] = {}
        self.current: Dict[int, "Ship"] = {}

    def incomingShip(self, s: "Ship") -> None:
        self.current[s.ID] = s
        self.history.setdefault(s.ID, s)

    def outgoingShip(self, s: "Ship") -> None:
        self.current.pop(s.ID, None)
        self.history.setdefault(s.ID, s)

    def put_container(self, cont: Container) -> None:
        self.containers[cont.ID] = cont

    def take_container(self, cont_id: int) -> Optional[Container]:
        # вилучення через pop()
        return self.containers.pop(cont_id, None)

    def has_container(self, cont_id: int) -> bool:
        return cont_id in self.containers

    def getDistance(self, other: "Port") -> float:
        R = 6371.0
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.latitude)
        lon2 = math.radians(other.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))
