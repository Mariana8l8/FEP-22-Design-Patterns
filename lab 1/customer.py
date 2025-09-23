from bill import Bill
from operators import Operator

class Customer:
    def __init__(self, ID, name, age, operators, bills, limitingAmount):
        self.ID = ID
        self.name = name
        self.age = age
        self.operators = operators  # масив операторів
        self.bills = bills          # масив рахунків
        # Ініціалізація рахунку для цього клієнта
        if bills is None or len(bills) == 0:
            self.bills = [Bill(limitingAmount)]
        # Вибір першого оператора як поточного
        self.operator = operators[0] if operators else None
        self.bill = self.bills[0]

    def talk(self, minute, other):
        cost = self.operator.calculateTalkingCost(minute, self)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f"{self.name} говорив з {other.name} {minute} хвилин. Вартість: {cost:.2f}")
        else:
            print(f"{self.name} не може говорити — перевищено ліміт!")

    def message(self, quantity, other):
        cost = self.operator.calculateMessageCost(quantity, self, other)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f"{self.name} відправив {quantity} повідомлень {other.name}. Вартість: {cost:.2f}")
        else:
            print(f"{self.name} не може відправити повідомлення — перевищено ліміт!")

    def connection(self, amount):
        cost = self.operator.calculateNetworkCost(amount)
        if self.bill.check(cost):
            self.bill.add(cost)
            print(f"{self.name} використав {amount} MB інтернету. Вартість: {cost:.2f}")
        else:
            print(f"{self.name} не може підключитися — перевищено ліміт!")

    def payBill(self, amount):
        self.bill.pay(amount)
        print(f"{self.name} оплатив {amount}. Поточний борг: {self.bill.getCurrentDebt():.2f}")

    def changeOperator(self, newOperator):
        self.operator = newOperator
        print(f"{self.name} змінив оператора на {newOperator.ID}")

    def changeBillLimit(self, amount):
        self.bill.changeTheLimit(amount)
        print(f"{self.name} змінив ліміт рахунку на {amount}")

    # Гетери та сетери
    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def getOperators(self):
        return self.operators

    def setOperators(self, operators):
        self.operators = operators

    def getBills(self):
        return self.bills

    def setBills(self, bills):
        self.bills = bills