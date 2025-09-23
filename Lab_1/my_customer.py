from utils import check_amount
from bill import Bill
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_operator import Operator

class Customer:
    customers: dict[int, 'Customer'] = {}

    def __init__(self, name: str, age: int):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 1:
            raise ValueError("Age must be greater than 0")

        self.__name: str = name
        self.__age: int = age
        self.__operator: dict[int, 'Operator'] = {}
        self.__bill: Bill = Bill(limitingAmount=0.0, currentDebt=0.0)

        if Customer.customers:
            self.__ID: int = max(Customer.customers.keys()) + 1
        else:
            self.__ID: int = 1
        Customer.customers[self.__ID] = self

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
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if age > 0:
            self.__age = age

    @property
    def operator(self):
        return self.__operator

    @property
    def bill(self):
        return self.__bill

    def _check_operator(self, customer: 'Customer', units: int) -> bool:
        if not self.__operator:
            print(f"{self.__name} does not have an operator assigned.")
            return True
        if not customer.operator:
            print(f"{customer.name} does not have an operator assigned.")
            return True
        if check_amount(units):
            return True
        return False

    def talk(self, minute: int, customer: 'Customer', operator_id: int):
        if self._check_operator(customer, minute):
            return

        total_cost = self.__operator[operator_id].calculate_talking_cost(minute, customer, operator_id)
        available_limit = self.__bill.limitingAmount - self.__bill.currentDebt
        cost_per_minute = self.__operator[operator_id].talkingCharge

        if total_cost <= available_limit:
            self.__bill.add(total_cost)
            print(f"{self.name} talked with {customer.name} for {minute} minutes. Cost: {total_cost:.2f}")
        elif available_limit == 0:
            print(
                f"{self.name} cannot make a call; credit limit reached ({self.__bill.currentDebt:.2f}/{self.__bill.limitingAmount:.2f}).")
        else:
            max_minutes = int(available_limit // cost_per_minute)
            self.__bill.add(available_limit)
            print(
                f"{self.name}'s call with {customer.name} was cut after {max_minutes} minutes. Limit reached ({self.__bill.limitingAmount:.2f}).")

    def message(self, quantity: int, customer: 'Customer', operator_id: int):
        if self._check_operator(customer, quantity):
            return

        total_cost = self.__operator[operator_id].calculate_message_cost(quantity, customer, operator_id)
        available_limit = self.__bill.limitingAmount - self.__bill.currentDebt
        cost_per_message = self.__operator[operator_id].messageCost

        if total_cost <= available_limit:
            self.__bill.add(total_cost)
            print(f"{self.name} sent {quantity} messages to {customer.name}. Cost: {total_cost:.2f}")
        elif available_limit == 0:
            print(
                f"{self.name} cannot send messages; credit limit reached ({self.__bill.currentDebt:.2f}/{self.__bill.limitingAmount:.2f}).")
        else:
            max_messages = int(available_limit // cost_per_message)
            self.__bill.add(available_limit)
            print(
                f"{self.name} could only send {max_messages} messages to {customer.name}. Limit reached ({self.__bill.limitingAmount:.2f}).")

    def connection(self, amount: float, operator_id: int):
        if not self.operator:
            print(f"{self.name} does not have an operator assigned.")
            return
        if check_amount(amount):
            return

        total_cost = self.__operator[operator_id].calculate_connection_cost(amount)
        available_limit = self.__bill.limitingAmount - self.__bill.currentDebt

        if total_cost <= available_limit:
            self.__bill.add(total_cost)
            print(f"{self.name} used {amount:.2f} MB of internet. Cost: {total_cost:.2f}")
        elif available_limit == 0:
            print(
                f"{self.name} cannot use internet; credit limit reached ({self.__bill.currentDebt:.2f}/{self.__bill.limitingAmount:.2f}).")
        else:
            max_amount = available_limit / self.__operator[operator_id].networkCharge
            self.__bill.add(available_limit)
            print(
                f"{self.name} could only use {max_amount:.2f} MB of internet. Limit reached ({self.__bill.limitingAmount:.2f}).")

    def check_debt(self):
        print(f"{self.name}'s current debt: {self.__bill.currentDebt:.2f}, limit: {self.__bill.limitingAmount:.2f}")

    def pay(self, amount: float):
        if check_amount(amount):
            return
        self.__bill.pay(amount)
        print(
            f"{self.name} paid {amount:.2f}. Current debt: {self.__bill.currentDebt:.2f}, limit: {self.__bill.limitingAmount:.2f}")

    def connect_operator(self, operator: 'Operator'):
        self.__operator[operator.ID] = operator
        typical_talk_minutes = 120
        typical_messages = 100
        typical_internet_mb = 2000

        limiting_amount = (
                operator.talkingCharge * typical_talk_minutes +
                operator.messageCost * typical_messages +
                operator.networkCharge * typical_internet_mb
        )

        self.__bill.changeTheLimitingAmount(limiting_amount)

        print(f"{self.__name} connected to operator {operator.ID}. "
              f"Limiting amount set to {self.__bill.limitingAmount:.2f}.")

    def disconnect_operator(self, operator_id: int):
        if not self.__operator:
            print(f"{self.__name} is not connected to any operator.")
            return

        operator_name = self.__operator.pop(operator_id).name
        if not self.__operator:
            self.__bill.changeTheLimitingAmount(0)
        print(f"{self.__name} has disconnected from operator {operator_name}. Limiting amount reset to 0.")