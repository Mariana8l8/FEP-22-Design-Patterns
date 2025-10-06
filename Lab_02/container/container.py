from abc import ABC, abstractmethod

class Container(ABC):
    def __init__(self, weight: int):
        if weight <= 0:
            raise ValueError("Container weight must be positive")
        self.weight = weight

        cls = type(self)
        if not hasattr(cls, "_id_counter"):
            cls._id_counter = 0
        self.ID = cls._id_counter
        cls._id_counter += 1

    @abstractmethod
    def consumption(self) -> float:
        ...


class BasicContainer(Container):
    def consumption(self) -> float:
        return 2.50 * self.weight


class HeavyContainer(Container):
    def consumption(self) -> float:
        return 3.00 * self.weight


class RefrigeratedContainer(Container):
    def consumption(self) -> float:
        return 5.00 * self.weight


class LiquidContainer(Container):
    def consumption(self) -> float:
        return 4.00 * self.weight
