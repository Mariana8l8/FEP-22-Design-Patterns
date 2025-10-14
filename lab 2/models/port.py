from .interfaces import IPort
import math

class Port(IPort):
    def __init__(self, port_id, latitude, longitude):
        self.id = port_id
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current = []

    def get_distance(self, other):
        return math.sqrt((self.latitude - other.latitude) ** 2 + (self.longitude - other.longitude) ** 2)

    def incoming_ship(self, ship):
        if ship not in self.current:
            self.current.append(ship)
        if ship not in self.history:
            self.history.append(ship)

    def outgoing_ship(self, ship):
        if ship in self.current:
            self.current.remove(ship)
