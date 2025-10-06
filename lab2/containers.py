from abc import ABC, abstractmethod

class Container(ABC):
    def __init__(self, ID: int, weight: int):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        pass

    @abstractmethod
    def equals(self, other) -> bool:
        pass


class BasicContainer(Container):
    def consumption(self) -> float:
        return self.weight * 2.5

    def equals(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.ID == other.ID and self.weight == other.weight
    

class HeavyContainer(Container):
    def consumption(self) -> float:
        return self.weight * 3

    def equals(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.ID == other.ID and self.weight == other.weight
    

class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 5

    def equals(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.ID == other.ID and self.weight == other.weight
    

class LiquidContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 4

    def equals(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.ID == other.ID and self.weight == other.weight