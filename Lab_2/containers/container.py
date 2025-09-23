from abc import ABC, abstractmethod
from id_generator import IDGenerator


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
