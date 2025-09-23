from utils import check_amount

class Bill:
    def __init__(self, limitingAmount: float, currentDebt: float):
        if not isinstance(limitingAmount, (int, float)):
            raise TypeError("limitingAmount must be a number")
        if not isinstance(currentDebt, (int, float)):
            raise TypeError("currentDebt must be a number")

        self.__limitingAmount: float = limitingAmount
        self.__currentDebt: float = currentDebt

    @property
    def limitingAmount(self):
        return self.__limitingAmount

    @property
    def currentDebt(self):
        return self.__currentDebt

    def check(self, amount: float) -> bool:
        if check_amount(amount):
            return False
        return (self.__currentDebt + amount) <= self.__limitingAmount

    def add(self, amount: float):
        if check_amount(amount):
            return

        self.__currentDebt += amount

    def pay(self, amount: float):
        if check_amount(amount):
            return

        self.__currentDebt -= amount

    def changeTheLimitingAmount(self, amount: float):
        if check_amount(amount):
            return

        self.__limitingAmount = amount