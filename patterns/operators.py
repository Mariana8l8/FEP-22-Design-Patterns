class Operator:
    def __init__(self, id, name, talkingCharge, messageCost, networkCharge, discountRate):
        self.id = id
        self.name = name
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate

    def calculateTalkingCost(self, minute, customer):
        cost = minute * self.talkingCharge
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discountRate)
        return cost

    def calculateMessageCost(self, quantity, customer, other):
        cost = quantity * self.messageCost
        if customer.operator.id == other.operator.id:
            cost *= (1 - self.discountRate)
        return cost

    def calculateNetworkCost(self, amount):
        return amount * self.networkCharge