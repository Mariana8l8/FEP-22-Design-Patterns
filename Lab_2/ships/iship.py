from __future__ import annotations
from abc import ABC, abstractmethod
from containers.container import Container
from id_generator import IDGenerator
from ports.iport import IPort


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