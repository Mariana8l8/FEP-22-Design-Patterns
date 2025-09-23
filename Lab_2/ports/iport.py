from __future__ import annotations
from abc import ABC, abstractmethod
from id_generator import IDGenerator
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ships.iship import IShip


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