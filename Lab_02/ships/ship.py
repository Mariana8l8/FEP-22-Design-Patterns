from typing import List, Optional
from typing import Dict
from container.container import (
    Container,
    BasicContainer,
    HeavyContainer,
    RefrigeratedContainer,
    LiquidContainer
)
from ships.capacity import ShipCapacity


class _AutoIDMixin:
    def _assign_id(self):
        cls = type(self)
        if not hasattr(cls, "_id_counter"):
            cls._id_counter = 0
        self.ID = cls._id_counter
        cls._id_counter += 1


class Ship(_AutoIDMixin):
    def __init__(self, currentPort, capacity: ShipCapacity, fuelPerKm: float = 0.0):
        self._assign_id()
        self.fuel = 0.0
        self.currentPort = currentPort
        self.capacity = capacity
        self.fuelPerKm = fuelPerKm
        self._containers: Dict[int, Container] = {}

        if hasattr(currentPort, "incomingShip"):
            currentPort.incomingShip(self)

    def _count_all(self) -> int: return len(self._containers)
    def _count_basic(self) -> int: return sum(isinstance(c, BasicContainer) for c in self._containers.values())
    def _count_heavy(self) -> int: return sum(isinstance(c, HeavyContainer) for c in self._containers.values())
    def _count_refrig(self) -> int: return sum(isinstance(c, RefrigeratedContainer) for c in self._containers.values())
    def _count_liquid(self) -> int: return sum(isinstance(c, LiquidContainer) for c in self._containers.values())
    def _weight(self) -> int: return sum(c.weight for c in self._containers.values())
    def _containers_consumption(self) -> float: return sum(c.consumption() for c in self._containers.values())

    def getCurrentContainers(self) -> List[Container]:
        return [self._containers[k] for k in sorted(self._containers)]

    def load(self, cont_id: int) -> bool:
        port = self.currentPort
        if not hasattr(port, "has_container") or not hasattr(port, "take_container") or not hasattr(port, "put_container"):
            return False

        if not port.has_container(cont_id):
            return False

        cont = port.take_container(cont_id)
        if cont is None:
            return False

        cap = self.capacity
        if self._count_all() + 1 > cap.max_all:
            port.put_container(cont); return False
        if self._weight() + cont.weight > cap.total_weight_capacity:
            port.put_container(cont); return False
        if isinstance(cont, BasicContainer) and (self._count_basic() + 1 > cap.max_basic):
            port.put_container(cont); return False
        if isinstance(cont, HeavyContainer) and (self._count_heavy() + 1 > cap.max_heavy):
            port.put_container(cont); return False
        if isinstance(cont, RefrigeratedContainer) and (self._count_refrig() + 1 > cap.max_refrig):
            port.put_container(cont); return False
        if isinstance(cont, LiquidContainer) and (self._count_liquid() + 1 > cap.max_liquid):
            port.put_container(cont); return False

        self._containers[cont.ID] = cont
        return True

    def unLoad(self, cont_id: int) -> bool:
        if cont_id not in self._containers:
            return False
        cont = self._containers.pop(cont_id)
        if hasattr(self.currentPort, "put_container"):
            self.currentPort.put_container(cont)
        return True

    def reFuel(self, amount: float) -> None:
        if amount > 0:
            self.fuel += amount

    def sailTo(self, newPort) -> bool:
        if newPort is self.currentPort:
            return True

        if not hasattr(self.currentPort, "getDistance"):
            return False

        dist = self.currentPort.getDistance(newPort)
        need = (self.fuelPerKm + self._containers_consumption()) * dist
        if self.fuel < need:
            return False

        self.fuel -= need

        if hasattr(self.currentPort, "outgoingShip"):
            self.currentPort.outgoingShip(self)
        self.currentPort = newPort
        if hasattr(newPort, "incomingShip"):
            newPort.incomingShip(self)
        return True
