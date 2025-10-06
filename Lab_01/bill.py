from utils import check_amount

class Bill:
    def __init__(self, limitingAmount: float | None = None, currentDebt: float | None = None, *,
                 limit: float | None = None, debt: float | None = None):
        if limit is not None:
            limitingAmount = limit
        if debt is not None:
            currentDebt = debt

        if limitingAmount is None:
            limitingAmount = 0.0
        if currentDebt is None:
            currentDebt = 0.0

        try:
            self._limit = float(limitingAmount)
            self._debt = float(currentDebt)
        except (TypeError, ValueError):
            raise TypeError("Limit and debt must be numeric")

        if self._limit < 0:
            raise ValueError("Limit must be non-negative")

    @property
    def limitingAmount(self) -> float:
        return self._limit

    @property
    def currentDebt(self) -> float:
        return self._debt

    @property
    def limit(self) -> float:
        return self._limit

    @property
    def debt(self) -> float:
        return self._debt

    def check(self, amount: float) -> bool:
        if check_amount(amount):
            return False
        return (self._debt + amount) <= self._limit

    def add(self, amount: float) -> None:
        if check_amount(amount):
            return
        self._debt += amount

    def pay(self, amount: float) -> None:
        if check_amount(amount):
            return
        self._debt -= amount

    def changeTheLimitingAmount(self, amount: float) -> None:
        if check_amount(amount):
            return
        self._limit = float(amount)
