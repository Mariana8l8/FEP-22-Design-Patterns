from math import sqrt

class Port:
    def __init__(self, ID: int, latitude: float, longitude : float):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.current = []
        self.history = []

    def incomingShip(self, ship):
        # Перевірка чи ship є у списку current за ID
        if not any(s.ID == ship.ID for s in self.current):
            self.current.append(ship)
        if not any(s.ID == ship.ID for s in self.history):
            self.history.append(ship)

    def outgoingShip(self, ship):
        if ship in self.current:
            self.current.remove(ship)
        ship.currentPort = None

    def getDistance(self, other) -> float:
        dx = self.latitude - other.latitude
        dy = self.longitude - other.longitude
        return sqrt(dx*dx + dy*dy)