from __future__ import annotations

import json
from dataclasses import dataclass
import math
from abc import ABC, abstractmethod
from pprint import pprint


class IDGenerator:
    __counters: dict[int, object] = {}
    __last_id: int = 0

    def register(self, instance: object) -> int:
        self.__last_id += 1
        self.__counters[self.__last_id] = instance
        return self.__last_id


class IPort(ABC):
    __id_generator: IDGenerator = IDGenerator()

    def __init__(self, latitude: float, longitude: float) -> None:
        if not isinstance(latitude, float) or not isinstance(longitude, float):
            raise TypeError("Latitude and longitude must be floats")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        self.__latitude = latitude
        self.__longitude = longitude
        self.__ID = IPort.__id_generator.register(self)

    @property
    def id(self) -> int:
        return self.__ID

    @property
    def latitude(self) -> float:
        return self.__latitude

    @property
    def longitude(self) -> float:
        return self.__longitude

    @abstractmethod
    def _incoming_ship(self, ship: IShip) -> None:
        pass

    @abstractmethod
    def _outgoing_ship(self, ship: IShip) -> None:
        pass


class Port(IPort):
    def __init__(self, latitude: float, longitude: float) -> None:
        super().__init__(latitude, longitude)
        self.__containers: list[Container] = []
        self.__history_ships: list[IShip] = []
        self.__current_ships: list[IShip] = []

    @property
    def containers(self) -> list[Container]:
        return self.__containers

    @property
    def history_ships(self) -> list[IShip]:
        return self.__history_ships

    @property
    def current_ships(self) -> list[IShip]:
        return self.__current_ships

    def _incoming_ship(self, ship: IShip) -> None:
        if not isinstance(ship, IShip):
            raise TypeError("Ship must be an instance of Ship")
        if ship in self.__current_ships:
            raise ValueError("Ship already incoming")

        self.__history_ships.append(ship)
        self.__current_ships.append(ship)

    def _outgoing_ship(self, ship: IShip) -> None:
        if not isinstance(ship, IShip):
            raise TypeError("Ship must be an instance of Ship")
        if ship not in self.__current_ships:
            raise ValueError("Ship already outgoing")

        self.__current_ships.remove(ship)

    def get_distance(self, port: IPort) -> float:
        if not isinstance(port, IPort):
            raise TypeError("Port must be an instance of Port")

        R = 6371.0

        lat1_rad = math.radians(self.latitude)
        lon1_rad = math.radians(self.longitude)
        lat2_rad = math.radians(port.latitude)
        lon2_rad = math.radians(port.longitude)

        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        central_angle = 2 * math.asin(math.sqrt(a))

        distance_km = R * central_angle
        return distance_km

    def load_container(self, container: Container) -> None:
        if not isinstance(container, Container):
            raise TypeError("Container must be an instance of Container")
        if container in self.__containers:
            raise ValueError("Container already incoming")

        self.__containers.append(container)

    def unload_container(self, container: Container) -> None:
        if not isinstance(container, Container):
            raise TypeError("Container must be an instance of Container")
        if container not in self.__containers:
            raise ValueError("Container not incoming")

        self.__containers.remove(container)

    def to_dict(self) -> dict:
        ships_dict = {}
        for ship in self.__current_ships:
            ships_dict.update(ship.to_dict())

        return {
            f"Port_{self.id}": {
                "lat": round(self.latitude, 2),
                "lon": round(self.longitude, 2),
                "basic_container": [c.id for c in self.__containers if isinstance(c, BasicContainer)],
                "heavy_container": [c.id for c in self.__containers if isinstance(c, HeavyContainer)],
                "liquid_container": [c.id for c in self.__containers if isinstance(c, LiquidContainer)],
                "refrigerated_container": [c.id for c in self.__containers if isinstance(c, RefrigeratedContainer)],
                **ships_dict
            }
        }


class IShip(ABC):
    __id_generator: IDGenerator = IDGenerator()

    def __init__(self) -> None:
        self.__ID = IShip.__id_generator.register(self)

    @property
    def id(self) -> int:
        return self.__ID

    @abstractmethod
    def sail_to(self, port: IPort) -> None:
        pass

    @abstractmethod
    def _re_fuel(self, fuel_deficit: float) -> None:
        pass

    @abstractmethod
    def load(self, container: Container) -> None:
        pass

    @abstractmethod
    def unload(self, container: Container) -> None:
        pass


@dataclass
class ShipCapacity:
    max_weight: int
    max_all: int
    max_basic: int
    max_heavy: int
    max_refrigerated: int
    max_liquid: int

    def to_dict(self) -> dict:
        return {
            "max_weight": self.max_weight,
            "max_all": self.max_all,
            "max_basic": self.max_basic,
            "max_heavy": self.max_heavy,
            "max_refrigerated": self.max_refrigerated,
            "max_liquid": self.max_liquid,
        }


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
        self.__containers: list[Container] = []
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
    def containers(self) -> list[Container]:
        return self.__containers

    @property
    def fuel_consumption_per_km(self) -> float:
        return self.__fuel_consumption_per_km

    @property
    def capacity(self) -> ShipCapacity:
        return self.__capacity

    @property
    def current_containers(self) -> list[Container]:
        return sorted(self.__containers, key=lambda c: c.id)

    @property
    def total_fuel_consumption(self) -> float:
        return self.__fuel_consumption_per_km + sum(c.consumption() for c in self.__containers)

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
        if sum(c.weight for c in self.__containers) + container.weight > self.__capacity.max_weight:
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
        self.__containers.append(container)

    def unload(self, container: Container) -> None:
        if not isinstance(container, Container):
            raise TypeError("Container must be an instance of Container")
        if container not in self.__containers:
            raise ValueError("Container not incoming")

        self.__containers.remove(container)
        self.__current_port.load_container(container)

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


class Container(ABC):
    __id_generator: IDGenerator = IDGenerator()

    def __init__(self, weight: int) -> None:
        if not isinstance(weight, int):
            raise TypeError("Weight must be an integer")
        if weight < 0:
            raise ValueError("Weight must be positive")

        self.__weight = weight
        self.__ID = Container.__id_generator.register(self)

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def id(self) -> int:
        return self.__ID

    @abstractmethod
    def consumption(self) -> float:
        pass


class BasicContainer(Container):
    def __init__(self, weight: int) -> None:
        if weight > 3000:
            raise ValueError("Weight must be less than or equal to 3000 units")
        super().__init__(weight)

    def consumption(self) -> float:
        return self.weight * 2.5


class HeavyContainer(Container):
    def __init__(self, weight: int) -> None:
        if weight <= 3000:
            raise ValueError("Weight must be greater than 3000 units")
        super().__init__(weight)

    def consumption(self) -> float:
        return self.weight * 3.0


class RefrigeratedContainer(HeavyContainer):

    def consumption(self) -> float:
        return self.weight * 5.0


class LiquidContainer(HeavyContainer):

    def consumption(self) -> float:
        return self.weight * 4.0


port1 = Port(latitude=50.45, longitude=30.52)
port2 = Port(latitude=48.85, longitude=2.35)

capacity1 = ShipCapacity(max_weight=10000, max_all=5, max_basic=2, max_heavy=2, max_refrigerated=1, max_liquid=1)
capacity2 = ShipCapacity(max_weight=15000, max_all=6, max_basic=3, max_heavy=2, max_refrigerated=1, max_liquid=2)

ship1 = Ship(fuel=5000.0, port=port1, fuel_consumption_per_km=10.0, capacity=capacity1)
ship2 = Ship(fuel=8000.0, port=port1, fuel_consumption_per_km=12.0, capacity=capacity2)

basic1 = BasicContainer(weight=2000)
basic2 = BasicContainer(weight=2500)
heavy1 = HeavyContainer(weight=4000)
refrigerated1 = RefrigeratedContainer(weight=5000)
liquid1 = LiquidContainer(weight=4500)

port1.load_container(basic1)
port1.load_container(basic2)
port1.load_container(heavy1)
port1.load_container(refrigerated1)
port1.load_container(liquid1)

ship1.load(basic1)
ship1.load(heavy1)

ship2.load(basic2)
ship2.load(refrigerated1)
ship2.load(liquid1)

pprint({
    **port1.to_dict(),
    **port2.to_dict(),
})

ship1.sail_to(port2)
ship2.sail_to(port2)

ship1.unload(basic1)
ship1.unload(heavy1)

ship2.unload(refrigerated1)
ship2.unload(liquid1)

ports_data = {
    **port1.to_dict(),
    **port2.to_dict(),
}

pprint(ports_data)

with open("ports_data.json", "w", encoding="utf-8") as f:
    json.dump(ports_data, f, ensure_ascii=False, indent=4)
