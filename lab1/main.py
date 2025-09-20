class Customer:
    def __init__(self, id, name, age, operator_id, bill_id):
        self.id = id
        self.name = name
        self.age = age
        self.operator_id = operator_id
        self.bill_id = bill_id

class Operator:
    def __init__(self, id, name, talk_cost, msg_cost, net_cost):
        self.id = id
        self.name = name
        self.talk_cost = talk_cost
        self.msg_cost = msg_cost
        self.net_cost = net_cost

class Bill:
    def __init__(self, id, limit, debt):
        self.id = id
        self.limit = limit
        self.debt = debt

def main():
    
    return

if __name__ == "__main__":
    main()