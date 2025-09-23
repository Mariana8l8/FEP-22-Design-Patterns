from __future__ import annotations
import math
from containers.basic import BasicContainer
from containers.container import Container
from containers.heavy import HeavyContainer
from containers.liquid import LiquidContainer
from containers.refrigerated import RefrigeratedContainer
from ports.iport import IPort
from ships.iship import IShip


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