from containers.heavy import HeavyContainer


class LiquidContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 4.0
