from containers import Container, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer

class Ship:
    def __init__(self, ID : int, fuel : float, totalWeightCapacity, maxNumberOfAllContainers, maxNumberOfHeavyContainers, maxNumberOfRefrigeratedContainers, maxNumberOfLiquidContainers, fuelConsumptionPerKM, currentPort = None):
        self.ID = ID
        self.fuel = fuel
        self.totalWeightCapacity = totalWeightCapacity
        self.maxNumberOfAllContainers = maxNumberOfAllContainers
        self.maxNumberOfHeavyContainers = maxNumberOfHeavyContainers
        self.maxNumberOfRefrigeratedContainers = maxNumberOfRefrigeratedContainers
        self.maxNumberOfLiquidContainers = maxNumberOfLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.currentPort = currentPort
        self.containers = []

    def sailTo(self, destinationPort) -> bool:
        distance = self.currentPort.getDistance(destinationPort)
        # Витрати на корабель
        fuelNeeded = distance * self.fuelConsumptionPerKM
        # Додаємо витрати контейнерів без множення на distance
        fuelNeeded += sum(c.consumption() for c in self.containers)

        if self.fuel >= fuelNeeded:
            self.currentPort.outgoingShip(self)
            destinationPort.incomingShip(self)
            self.fuel -= fuelNeeded
            self.currentPort = destinationPort
            return True
        else:
            return False

    def reFuel(self, newFuel):
        self.fuel += newFuel

    def load(self, container) -> bool:
        currentWeight = sum(c.weight for c in self.containers)
        if currentWeight + container.weight > self.totalWeightCapacity:
            return False
        if len(self.containers) + 1 > self.maxNumberOfAllContainers:
            return False

        if isinstance(container, RefrigeratedContainer):
            refrigerated_count = sum(isinstance(c, RefrigeratedContainer) for c in self.containers)
            if refrigerated_count + 1 > self.maxNumberOfRefrigeratedContainers:
                return False
        if isinstance(container, LiquidContainer):
            liquid_count = sum(isinstance(c, LiquidContainer) for c in self.containers)
            if liquid_count + 1 > self.maxNumberOfLiquidContainers:
                return False
        if isinstance(container, HeavyContainer):
            heavy_count = sum(isinstance(c, HeavyContainer) for c in self.containers)
            if heavy_count + 1 > self.maxNumberOfHeavyContainers:
                return False

        self.containers.append(container)
        return True

    def unLoad(self, container) -> bool:
        if container in self.containers:
            self.containers.remove(container)  # видаляємо контейнер
            return True
        else:
            return False
