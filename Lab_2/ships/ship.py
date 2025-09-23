from __future__ import annotations
from containers.basic import BasicContainer
from containers.container import Container
from containers.heavy import HeavyContainer
from containers.liquid import LiquidContainer
from containers.refrigerated import RefrigeratedContainer
from ports.iport import IPort
from ports.port import Port
from ships.iship import IShip
from ships.ship_capacity import ShipCapacity


class Ship(IShip):
    def __init__(self, fuel: float, port: Port, fuel_consumption_per_km: float, capacity: ShipCapacity) -> None:
        super().__init__()
        if not isinstance(port, IPort):
            raise TypeError("Port must be an instance of Port")
        if not isinstance(fuel_consumption_per_km, float):
            raise TypeError("Fuel_consumption_per_km must be floats")
        if not isinstance(capacity, ShipCapacity):
            raise TypeError("Capacity must be an instance of ShipCapacity")
        if not isinstance(fuel, float):
            raise TypeError("Fuel must be floats")
        if not 0 <= fuel:
            raise ValueError("Fuel must be positive")

        self.__fuel = fuel
        self.__current_port: Port = port
        self.__containers: dict[int, Container] = {}
        self.__fuel_consumption_per_km: float = fuel_consumption_per_km
        self.__capacity: ShipCapacity = capacity

        self.__current_port._incoming_ship(self)

    @property
    def fuel(self) -> float:
        return self.__fuel

    @property
    def current_port(self) -> Port:
        return self.__current_port

    @property
    def containers(self) -> dict[int, Container]:
        return self.__containers

    @property
    def fuel_consumption_per_km(self) -> float:
        return self.__fuel_consumption_per_km

    @property
    def capacity(self) -> ShipCapacity:
        return self.__capacity

    @property
    def current_containers(self) -> list[Container]:
        return sorted(self.__containers.values(), key=lambda c: c.id)

    @property
    def total_fuel_consumption(self) -> float:
        return self.__fuel_consumption_per_km + sum(c.consumption() for c in self.__containers.values())

    def sail_to(self, port: IPort) -> None:
        if not isinstance(port, IPort):
            raise TypeError("Port must be an instance of Port")

        required_fuel = self.__current_port.get_distance(port) * self.total_fuel_consumption
        if required_fuel > self.__fuel:
            self._re_fuel(required_fuel - self.__fuel)
            print(f"Ship_{self.id} refueled with enough fuel to reach the destination.")

        self.__fuel -= required_fuel
        self.__current_port._outgoing_ship(self)
        self.__current_port = port
        self.__current_port._incoming_ship(self)

    def _re_fuel(self, fuel_deficit: float) -> None:
        self.__fuel = (self.__fuel + fuel_deficit) * 1.5

    def load(self, container: Container) -> None:
        if not isinstance(container, Container):
            raise TypeError("Container must be an instance of Container")
        if container in self.__containers:
            raise ValueError("Container already loaded on the ship")

        if len(self.__containers) >= self.__capacity.max_all:
            print("Cannot load more containers: maximum number of containers reached.")
            return
        if sum(c.weight for c in self.__containers.values()) + container.weight > self.__capacity.max_weight:
            print("Cannot load container: total weight capacity exceeded.")
            return

        container_limits = {
            BasicContainer: self.__capacity.max_basic,
            HeavyContainer: self.__capacity.max_heavy,
            RefrigeratedContainer: self.__capacity.max_refrigerated,
            LiquidContainer: self.__capacity.max_liquid
        }

        for ctype, limit in container_limits.items():
            if isinstance(container, ctype):
                unit_count = sum(isinstance(c, ctype) for c in self.__containers)

                if unit_count >= limit:
                    print(f"Cannot load more {ctype.__name__} containers: limit of {limit} reached.")
                    return

        self.__current_port.unload_container(container)
        self.__containers[container.id] = container

    def unload(self, container_id: int) -> None:
        if not isinstance(container_id, int):
            raise TypeError("Container must be an instance of Container")
        if container_id not in self.__containers.keys():
            raise ValueError("Container not incoming")

        unload_container = self.__containers.pop(container_id)
        self.__current_port.load_container(unload_container)

    def to_dict(self) -> dict:
        return {
            f"ship_{self.id}": {
                "fuel": round(self.fuel, 2),
                **self.capacity.to_dict(),
                "basic_container": [c.id for c in self.__containers if isinstance(c, BasicContainer)],
                "heavy_container": [c.id for c in self.__containers if isinstance(c, HeavyContainer)],
                "liquid_container": [c.id for c in self.__containers if isinstance(c, LiquidContainer)],
                "refrigerated_container": [c.id for c in self.__containers if isinstance(c, RefrigeratedContainer)],
                "fuel_consumption_per_km": self.total_fuel_consumption
            }
        }
