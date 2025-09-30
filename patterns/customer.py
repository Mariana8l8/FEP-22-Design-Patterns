from bill import Bill

class Customer:
    def __init__(self, id, name, age, operator, bill):
        self.id = id
        self.name = name
        self.age = age
        self.operator = operator
        self.bill = bill

    def talk(self, minute, other):
        cost = self.operator.calculateTalkingCost(minute, self)
        if self.bill.add(cost):
            print(f"{self.name} зателефонував {other.name} на {minute} хв. Вартість: {cost:.2f} грн")
        else:
            print("Перевищено ліміт рахунку!")

    def message(self, quantity, other):
        cost = self.operator.calculateMessageCost(quantity, self, other)
        if self.bill.add(cost):
            print(f"{self.name} надіслав {quantity} повідомлень {other.name}. Вартість: {cost:.2f} грн")
        else:
            print("Перевищено ліміт рахунку!")

    def connection(self, amount):
        cost = self.operator.calculateNetworkCost(amount)
        if self.bill.add(cost):
            print(f"{self.name} використав {amount} МБ інтернету. Вартість: {cost:.2f} грн")
        else:
            print("Перевищено ліміт рахунку!")

    def payBill(self, amount):
        self.bill.pay(amount)
        print(f"{self.name} сплатив {amount} грн. Поточний борг: {self.bill.getCurrentDebt():.2f} грн")

    def changeOperator(self, new_operator):
        self.operator = new_operator
        print(f"{self.name} перейшов на оператора {new_operator.name}")


class Customer2:
    def __init__(self, id, name, age, operator, bill):
        self.id = id
        self.name = name
        self.age = age
        self.operator = operator
        self.bill = bill
    def talk(self, minute, other):
        cost = self.operator.calculateTalkingCost(minute, self)
        if self.bill.add(cost):
            print(f"{self.name} зателефонував {other.name} на {minute} хв. Вартість: {cost:.2f} грн")
        else:
            print("Перевищено ліміт рахунку!")
    def message(self, quantity, other):
        cost = self.operator.calculateMessageCost(quantity, self, other)
        if self.bill.add(cost):
            print(f"{self.name} надіслав {quantity} повідомлень {other.name}. Вартість: {cost:.2f} грн")
        else:
            print("Перевищено ліміт рахунку!")
    def connection(self, amount):
        cost = self.operator.calculateNetworkCost(amount)
        if self.bill.add(cost):
            print(f"{self.name} використав {amount} МБ інтернету. Вартість: {cost:.2f} грн")
        else:
            print("Перевищено ліміт рахунку!")
    def payBill(self, amount):
        self.bill.pay(amount)
        print(f"{self.name} сплатив {amount} грн. Поточний борг: {self.bill.getCurrentDebt():.2f} грн")
    def changeOperator(self, new_operator):
        self.operator = new_operator
        print(f"{self.name} перейшов на оператора {new_operator.name}")

    