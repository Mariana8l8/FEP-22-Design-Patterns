from .interfaces import IShip
from models.container import HeavyContainer, RefrigeratedContainer, LiquidContainer

class Ship(IShip):
    def __init__(self, ship_id, current_port, fuel, total_weight_capacity,
                 max_all, max_heavy, max_refrigerated, max_liquid, fuel_per_km):
        self.id = ship_id
        self.current_port = current_port
        self.fuel = fuel
        self.total_weight_capacity = total_weight_capacity
        self.max_all = max_all
        self.max_heavy = max_heavy
        self.max_refrigerated = max_refrigerated
        self.max_liquid = max_liquid
        self.fuel_per_km = fuel_per_km
        self.containers = []

    def refuel(self, amount):
        self.fuel += amount

    def load(self, container):
        if len(self.containers) >= self.max_all:
            return False
        if sum(c.weight for c in self.containers) + container.weight > self.total_weight_capacity:
            return False

        if isinstance(container, RefrigeratedContainer) and sum(isinstance(c, RefrigeratedContainer) for c in self.containers) >= self.max_refrigerated:
            return False
        if isinstance(container, LiquidContainer) and sum(isinstance(c, LiquidContainer) for c in self.containers) >= self.max_liquid:
            return False
        if isinstance(container, HeavyContainer) and sum(isinstance(c, HeavyContainer) for c in self.containers) >= self.max_heavy:
            return False

        if container in self.current_port.containers:
            self.current_port.containers.remove(container)
        self.containers.append(container)
        return True

    def unload(self, container):
        if container in self.containers:
            self.containers.remove(container)
            self.current_port.containers.append(container)
            return True
        return False

    def sail_to(self, destination):
        distance = self.current_port.get_distance(destination)
        total_consumption = (self.fuel_per_km + sum(c.consumption() for c in self.containers)) * distance

        if self.fuel < total_consumption:
            print(f"Ship {self.id} has insufficient fuel.")
            return False

        self.fuel -= total_consumption
        self.current_port.outgoing_ship(self)
        self.current_port = destination
        destination.incoming_ship(self)
        return True
