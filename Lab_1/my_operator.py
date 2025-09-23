from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_customer import Customer

class Operator:
    operators: dict[int, 'Operator'] = {}

    def __init__(self, name: str, talkingCharge: float | int, messageCost: float | int, networkCharge: float | int,
                 discountRate: int):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(talkingCharge, (int, float)):
            raise TypeError("talkingCharge must be a number")
        if not isinstance(messageCost, (int, float)):
            raise TypeError("messageCost must be a number")
        if not isinstance(networkCharge, (int, float)):
            raise TypeError("networkCharge must be a number")
        if not isinstance(discountRate, int):
            raise TypeError("discountRate must be an integer")

        self.__name: str = name
        self.__talkingCharge: float = talkingCharge
        self.__messageCost: float = messageCost
        self.__networkCharge: float = networkCharge
        self.__discountRate: int = discountRate

        if Operator.operators:
            self.__ID: int = max(Operator.operators.keys()) + 1
        else:
            self.__ID: int = 1
        Operator.operators[self.__ID] = self

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def talkingCharge(self):
        return self.__talkingCharge

    @talkingCharge.setter
    def talkingCharge(self, talkingCharge):
        self.__talkingCharge = talkingCharge

    @property
    def messageCost(self):
        return self.__messageCost

    @messageCost.setter
    def messageCost(self, messageCost):
        self.__messageCost = messageCost

    @property
    def networkCharge(self):
        return self.__networkCharge

    @networkCharge.setter
    def networkCharge(self, networkCharge):
        self.__networkCharge = networkCharge

    @property
    def discountRate(self):
        return self.__discountRate

    @discountRate.setter
    def discountRate(self, discountRate):
        self.__discountRate = discountRate

    def calculate_talking_cost(self, minute: int, customer2: 'Customer', operator_id: int) -> float:
        cost_per_minute = self.__talkingCharge
        if operator_id in customer2.operator.keys():
            cost_per_minute *= (100 - self.__discountRate) / 100
        return minute * cost_per_minute

    def calculate_message_cost(self, quantity: int, customer2: 'Customer', operator_id: int) -> float:
        cost_per_message = self.__messageCost
        if operator_id in customer2.operator.keys():
            cost_per_message *= (100 - self.__discountRate) / 100
        return quantity * cost_per_message

    def calculate_connection_cost(self, amount: float) -> float:
        return amount * self.__networkCharge