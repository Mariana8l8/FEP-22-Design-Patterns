class Customer:
    def __init__(self, id, name, age, operator_id, bill_id):
        self.id = id
        self.name = name
        self.age = age
        self.operator_id = operator_id
        self.bill_id = bill_id
        self.__bill = Bill(bill_id, 100, 0)


    def get_bill(self):
        return self.__bill

    def talk(self, minutes, operators, bills):
        cost = operators[self.operator_id - 1].calculate_talk_cost(minutes)
        if bills.check_limit(cost):
            bills.add(cost)
            debt = bills.get_debt()
            print(f"Вартість дзвінка: {cost} грн. Ваш борг: {debt} грн")
        else:
            print("Перевищено ліміт рахунку. Дзвінок не здійснено.")
    
    def message(self, quantity, operators, bills):
        cost = operators[self.operator_id - 1].calluclate_msg_cost(quantity)
        if bills.check_limit(cost):
            bills.add(cost)
            debt = bills.get_debt()
            print(f"Вартість повідомлення: {cost} грн. Ваш борг: {debt} грн")
        else:
            print("Перевищено ліміт рахунку. Повідомлення не відправлено.")

    def connect(self, amount, operators, bills):
        cost = operators[self.operator_id - 1].calculate_net_cost(amount)
        if bills.check_limit(cost):
            bills.add(cost)
            debt = bills.get_debt()
            print(f"Ви замовили {amount} МБ інтернету. Вартість: {debt} грн")
        else:
            print("Перевищено ліміт рахунку. Послуга не надана.")


class Operator:
    def __init__(self, id, name, talk_cost, msg_cost, net_cost):
        self.id = id
        self.name = name
        self.talk_cost = talk_cost
        self.msg_cost = msg_cost
        self.net_cost = net_cost

    def calculate_talk_cost(self, minutes):
        return self.talk_cost * minutes
        
    def calluclate_msg_cost(self, quantity):
        return self.msg_cost * quantity

    def calculate_net_cost(self, amount):
        return self.net_cost * amount
    

class Bill:
    def __init__(self, id, limit, debt):
        self.id = id
        self.limit = limit
        self.debt = debt

    def check_limit(self, cost):
        if cost + self.debt > self.limit:
            return False
        else:
            return True

    def add(self, amount):
        self.debt += amount
    
    def pay(self, amount):
        if amount > self.debt:
            print(f"Ви сплатили більше, ніж ваш борг. Ваш борг: {self.debt} грн")
        else:
            self.debt -= amount
            print(f"Ви сплатили {amount} грн. Залишок боргу: {self.debt} грн")

    def get_debt(self):
        return self.debt
    

def main():
    # Список операторів
    # 1 - id, 2 - name, 3 - talk_cost, 4 - msg_cost, 5 - net_cost
    operators = [
        Operator(1, "Lvivstar", 1.5, 0.5, 0.2),
        Operator(2, "Sikfone", 1.0, 0.7, 0.3),
        Operator(3, "Deathcell", 1.2, 0.6, 0.25)
    ]
    
    print(f"Доброго дня! Створимо вашого першого клієнта.")
    i = 1   # ID клієнта
    name = input("Введіть ім'я клієнта: ")
    age = int(input("Введіть вік клієнта: "))
    print("Оберіть оператора:")
    for operator in operators:
        print(f"{operator.id}. {operator.name}")
    operator_id = int(input("Введіть номер оператора: "))

    Customer1 = Customer(i, name, age, operator_id, i)
    bill1 = Customer1.get_bill()

    i += 1 # Наступний ID клієнта

    while True:
        print("\nОберіть дію:")
        print("1. Зателефонувати")
        print("2. Відправити повідомлення")
        print("3. Замовлення інтернету")
        print("4. Поповнити рахунок")
        print("5. Перевірити борг")
        print("6. Вийти")
        choice = input("Ваш вибір: ")

        if choice == '1':
            minutes = int(input("Введіть кількість хвилин: "))
            Customer1.talk(minutes, operators, bill1)
        elif choice == '2':
            quantity = int(input("Введіть кількість повідомлень: "))
            Customer1.message(quantity, operators, bill1)
        elif choice == '3':
            amount = float(input("Введіть кількість МБ: "))
            Customer1.connect(amount, operators, bill1)
        elif choice == '4':
            amount = float(input("Введіть суму для поповнення: "))
            bill1.pay(amount)
        elif choice == '5':
            print(f"Ваш борг: {bill1.get_debt()} грн")
        elif choice == '6':
            print("До побачення!")
            break


if __name__ == "__main__":
    main()