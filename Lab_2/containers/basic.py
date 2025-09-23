from containers.container import Container


class BasicContainer(Container):
    def __init__(self, weight: int) -> None:
        if weight > 3000:
            raise ValueError("Weight must be less than or equal to 3000 units")
        super().__init__(weight)

    def consumption(self) -> float:
        return self.weight * 2.5
