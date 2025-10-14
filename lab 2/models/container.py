from abc import ABC, abstractmethod

class Container(ABC):
    def __init__(self, container_id, weight):
        self.id = container_id
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id and self.weight == other.weight


class BasicContainer(Container):
    def consumption(self):
        return 2.5


class HeavyContainer(Container):
    def consumption(self):
        return 3.0


class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return 5.0


class LiquidContainer(HeavyContainer):
    def consumption(self):
        return 4.0
