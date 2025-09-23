class Operator:
    def __init__(self, ID, talkingCharge, messageCost, networkCharge, discountRate):
        self.ID = ID
        self.talkingCharge = talkingCharge
        self.messageCost = messageCost
        self.networkCharge = networkCharge
        self.discountRate = discountRate

    def calculateTalkingCost(self, minute, customer):
        cost = minute * self.talkingCharge
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discountRate / 100)
        return cost

    def calculateMessageCost(self, quantity, customer, other):
        cost = quantity * self.messageCost
        if customer.operator.ID == other.operator.ID:
            cost *= (1 - self.discountRate / 100)
        return cost

    def calculateNetworkCost(self, amount):
        return amount * self.networkCharge

    # Гетери та сетери
    def getTalkingCharge(self):
        return self.talkingCharge

    def setTalkingCharge(self, value):
        self.talkingCharge = value

    def getMessageCost(self):
        return self.messageCost

    def setMessageCost(self, value):
        self.messageCost = value

    def getNetworkCharge(self):
        return self.networkCharge

    def setNetworkCharge(self, value):
        self.networkCharge = value

    def getDiscountRate(self):
        return self.discountRate

    def setDiscountRate(self, value):
        self.discountRate = value
