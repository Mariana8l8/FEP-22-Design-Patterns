class Bill:
    def __init__(self, limitingAmount):
        self.limitingAmount = limitingAmount
        self.currentDebt = 0.0

    def check(self, amount):
        return self.currentDebt + amount <= self.limitingAmount

    def add(self, amount):
        if self.check(amount):
            self.currentDebt += amount
        else:
            print("Ліміт перевищено!")

    def pay(self, amount):
        if amount <= self.currentDebt:
            self.currentDebt -= amount
        else:
            self.currentDebt = 0.0

    def changeTheLimit(self, amount):
        self.limitingAmount = amount

    def getLimitingAmount(self):
        return self.limitingAmount

    def getCurrentDebt(self):
        return self.currentDebt
