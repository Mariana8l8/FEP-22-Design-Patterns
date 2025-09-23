from containers.heavy import HeavyContainer


class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 5.0
