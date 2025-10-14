from abc import ABC, abstractmethod

class IPort(ABC):
    @abstractmethod
    def incoming_ship(self, ship): pass

    @abstractmethod
    def outgoing_ship(self, ship): pass


class IShip(ABC):
    @abstractmethod
    def sail_to(self, port): pass

    @abstractmethod
    def refuel(self, amount): pass

    @abstractmethod
    def load(self, container): pass

    @abstractmethod
    def unload(self, container): pass
