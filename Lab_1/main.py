def check_amount(amount: float) -> bool:
    if amount < 0:
        print(f"Invalid usage amount: {amount}. Must be a positive value.")
        return True
    return False


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


class Operator:
    operators: dict[int, 'Operator'] = {}

    def __init__(self, name: str, talkingCharge: float, messageCost: float, networkCharge: float,
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

    def calculate_talking_cost(self, minute: int, customer1: 'Customer', customer2: 'Customer') -> float:
        cost_per_minute = self.__talkingCharge
        if customer1.operator.ID == customer2.operator.ID:
            cost_per_minute *= (100 - self.__discountRate) / 100
        return minute * cost_per_minute

    def calculate_message_cost(self, quantity: int, customer1: 'Customer', customer2: 'Customer') -> float:
        cost_per_message = self.__messageCost
        if customer1.operator.ID == customer2.operator.ID:
            cost_per_message *= (100 - self.__discountRate) / 100
        return quantity * cost_per_message

    def calculate_connection_cost(self, amount: float) -> float:
        return amount * self.__networkCharge


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
        self.__operator: Operator = None
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

    def talk(self, minute: int, customer: 'Customer'):
        if self._check_operator(customer, minute):
            return

        total_cost = self.__operator.calculate_talking_cost(minute, self, customer)
        available_limit = self.__bill.limitingAmount - self.__bill.currentDebt
        cost_per_minute = self.__operator.talkingCharge

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

    def message(self, quantity: int, customer: 'Customer'):
        if self._check_operator(customer, quantity):
            return

        total_cost = self.__operator.calculate_message_cost(quantity, self, customer)
        available_limit = self.__bill.limitingAmount - self.__bill.currentDebt
        cost_per_message = self.__operator.messageCost

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

    def connection(self, amount: float):
        if not self.operator:
            print(f"{self.name} does not have an operator assigned.")
            return
        if check_amount(amount):
            return

        total_cost = self.__operator.calculate_connection_cost(amount)
        available_limit = self.__bill.limitingAmount - self.__bill.currentDebt

        if total_cost <= available_limit:
            self.__bill.add(total_cost)
            print(f"{self.name} used {amount:.2f} MB of internet. Cost: {total_cost:.2f}")
        elif available_limit == 0:
            print(
                f"{self.name} cannot use internet; credit limit reached ({self.__bill.currentDebt:.2f}/{self.__bill.limitingAmount:.2f}).")
        else:
            max_amount = available_limit / self.__operator.networkCharge
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

    def connect_operator(self, operator: Operator):
        if self.__operator:
            print(f"You need to disconnect from operator {self.__operator.ID} first.")
            return

        self.__operator = operator
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

    def disconnect_operator(self):
        if not self.__operator:
            print(f"{self.__name} is not connected to any operator.")
            return

        operator_name = self.__operator.name
        self.__operator = None
        self.__bill.changeTheLimitingAmount(0)
        print(f"{self.__name} has disconnected from operator {operator_name}. Limiting amount reset to 0.")


op1 = Operator("Kyivstar", talkingCharge=2.0, messageCost=0.5, networkCharge=0.1, discountRate=10)
op2 = Operator("Vodafone", talkingCharge=3.0, messageCost=0.75, networkCharge=0.15, discountRate=15)
person1 = Customer('Oleg', 18)
person2 = Customer('Danko', 19)
person3 = Customer('Denis', 18)

print("\n=== Підключення операторів ===")
person1.connect_operator(op1)
person2.connect_operator(op2)
person3.connect_operator(op1)

print("\n=== Дзвінки ===")
person1.talk(10, person3)
person1.talk(50, person2)

print("\n=== Повідомлення ===")
person2.message(5, person3)
person3.message(10, person1)

print("\n=== Інтернет ===")
person1.connection(200)
person2.connection(800)

print("\n=== Борг ===")
person1.check_debt()
person2.check_debt()
person3.check_debt()

print("\n=== Оплата ===")
person2.pay(10)
person2.check_debt()

print("\n=== Відключення операторів ===")
person1.disconnect_operator()
person2.disconnect_operator()
person3.disconnect_operator()

print("\n=== Перевірка без оператора ===")
person1.talk(5, person2)

print("\n=== Борг ===")
person1.check_debt()
person2.check_debt()
person3.check_debt()