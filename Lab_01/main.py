from operator_logic import Operator
from customer_logic import Customer



def run_demo():
    opA = Operator("Lifecell", talkingCharge=1.9, messageCost=0.40, networkCharge=0.11, discountRate=12)
    opB = Operator("TriMob",   talkingCharge=2.8, messageCost=0.65, networkCharge=0.13, discountRate=5)

    #Customers
    marta = Customer("Marta", 22)
    yurii = Customer("Yurii", 28)
    lena  = Customer("Lena",  17)

    print("\n=== Connecting Operators ===")
    marta.connect_operator(opA)
    yurii.connect_operator(opA)
    yurii.connect_operator(opB)
    lena.connect_operator(opB)

    print("\n=== Internet Usage ===")
    marta.connection(120, opA.ID)
    yurii.connection(240, opA.ID)

    print("\n=== Messages ===")
    yurii.message(7, lena, opB.ID)
    marta.message(3, yurii, opA.ID)

    print("\n=== Calls ===")
    lena.talk(12, marta, opB.ID)
    marta.talk(6, yurii, opA.ID)

    print("\n=== Debts ===")
    marta.check_debt()
    print()
    yurii.check_debt()
    print()
    lena.check_debt()

    print("\n=== Payments ===")
    marta.pay(5, opA.ID)
    print()
    yurii.pay(8, opA.ID)

    print("\n=== Extra Actions ===")
    yurii.message(2, marta, opA.ID)

    print("\n=== Disconnections ===")
    lena.disconnect_operator(opB.ID)
    print()
    lena.talk(3, marta, opB.ID)  # attempt after disconnection

    print("\n=== Final Debts ===")
    marta.check_debt()
    print()
    yurii.check_debt()
    print()
    lena.check_debt()


if __name__ == "__main__":
    run_demo()
