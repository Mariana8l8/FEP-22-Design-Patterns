from typing import List, Optional
from math import isclose
from typing import Dict


from container.container import (
    Container,
    BasicContainer,
    HeavyContainer,
    RefrigeratedContainer,
    LiquidContainer
)
from ports.port import Port
from ships.capacity import ShipCapacity


class _AutoIDMixin:
    """Мікси для простої автогенерації ID без classmethod-ів."""
    def _assign_id(self):
        cls = type(self)
        if not hasattr(cls, "_id_counter"):
            cls._id_counter = 0
        self.ID = cls._id_counter
        cls._id_counter += 1


class Ship(_AutoIDMixin):
    """
    - Звичайний клас без dataclass та __post_init__
    - Генерація ID: один виклик self._assign_id()
    - load/unLoad працюють по ID контейнера
    - Зняття контейнера з порту — через port.take_container(cont_id) всередині якого має бути pop()
    """
    def __init__(self, currentPort, capacity: ShipCapacity, fuelPerKm: float = 0.0):
        self._assign_id()
        self.fuel = 0.0
        self.currentPort = currentPort
        self.capacity = capacity
        self.fuelPerKm = fuelPerKm
        self._containers: Dict[int, Container] = {}

        # зареєструвати корабель у порту (duck-typing: метод просто має існувати)
        if hasattr(currentPort, "incomingShip"):
            currentPort.incomingShip(self)

    # ---------- helpers ----------
    def _count_all(self) -> int: return len(self._containers)
    def _count_basic(self) -> int: return sum(isinstance(c, BasicContainer) for c in self._containers.values())
    def _count_heavy(self) -> int: return sum(isinstance(c, HeavyContainer) for c in self._containers.values())
    def _count_refrig(self) -> int: return sum(isinstance(c, RefrigeratedContainer) for c in self._containers.values())
    def _count_liquid(self) -> int: return sum(isinstance(c, LiquidContainer) for c in self._containers.values())
    def _weight(self) -> int: return sum(c.weight for c in self._containers.values())
    def _containers_consumption(self) -> float: return sum(c.consumption() for c in self._containers.values())

    # ---------- API ----------
    def getCurrentContainers(self) -> List[Container]:
        # відсортований за ID список
        return [self._containers[k] for k in sorted(self._containers)]

    def load(self, cont_id: int) -> bool:
        """
        Завантажити контейнер з поточного порту за його ID.
        Очікується, що в порті реалізовано:
          - has_container(id)
          - take_container(id) -> pop()
          - put_container(container)
        """
        port = self.currentPort
        if not hasattr(port, "has_container") or not hasattr(port, "take_container") or not hasattr(port, "put_container"):
            return False

        if not port.has_container(cont_id):
            return False

        cont = port.take_container(cont_id)  # ВАЖЛИВО: всередині має бути pop()
        if cont is None:
            return False

        cap = self.capacity
        # усі ліміти, включно з max_basic
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
        """Вивантажити контейнер за ID у поточний порт."""
        if cont_id not in self._containers:
            return False
        cont = self._containers.pop(cont_id)
        # покласти назад у порт
        if hasattr(self.currentPort, "put_container"):
            self.currentPort.put_container(cont)
        return True

    def reFuel(self, amount: float) -> None:
        if amount > 0:
            self.fuel += amount

    def sailTo(self, newPort) -> bool:
        """
        Перехід у інший порт:
          - потребує: currentPort.getDistance(newPort)
          - зменшує паливо на (fuelPerKm + sum(cont.cons)) * distance
          - викликає outgoingShip / incomingShip якщо вони є
        """
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
