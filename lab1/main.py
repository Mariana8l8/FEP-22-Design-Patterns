class Customer:
    def __init__(self, id, name, age, operator_id):
        self.id = id
        self.name = name
        self.age = age
        self.operator_id = operator_id   

class Bill:
    def __init__(self, id, limit):
        self.id = id
        self.limit = limit
        self.debt = 0

    def check_limit(self, cost):
        return self.debt + cost <= self.limit

    def add(self, amount):
        self.debt += amount

    def pay(self, amount):
        self.debt = max(0, self.debt - amount)

    def get_debt(self):
        return self.debt


class Operator:
    def __init__(self, id, name, talk_cost, msg_cost, net_cost):
        self.id = id
        self.name = name
        self.talk_cost = talk_cost
        self.msg_cost = msg_cost
        self.net_cost = net_cost
        self.bills = {}   # словник: customer_id -> Bill

    def create_bill(self, customer_id, limit=200):
        self.bills[customer_id] = Bill(customer_id, limit)
        print(f"Створено рахунок для клієнта {customer_id} в {self.name}")

    def _get_bill(self, customer_id):   #Для зовнішнього використання
        return self.bills.get(customer_id)

    def provide_talk(self, customer_id, minutes):
        bill = self._get_bill(customer_id)
        if not bill:
            print("Рахунок не знайдено")
            return
        cost = self.talk_cost * minutes
        if bill.check_limit(cost):
            bill.add(cost)
            print(f"Дзвінок {minutes} хв. Вартість: {cost} грн. Борг: {bill.get_debt()} грн")
        else:
            print("Перевищено ліміт рахунку.")

    def provide_message(self, customer_id, quantity):
        bill = self._get_bill(customer_id)
        if not bill:
            print("Рахунок не знайдено")
            return
        cost = self.msg_cost * quantity
        if bill.check_limit(cost):
            bill.add(cost)
            print(f"Повідомлення {quantity} шт. Вартість: {cost} грн. Борг: {bill.get_debt()} грн")
        else:
            print("Перевищено ліміт рахунку.")

    def provide_internet(self, customer_id, mb):
        bill = self._get_bill(customer_id)
        if not bill:
            print("Рахунок не знайдено")
            return
        cost = self.net_cost * mb
        if bill.check_limit(cost):
            bill.add(cost)
            print(f"Інтернет {mb} МБ. Вартість: {cost} грн. Борг: {bill.get_debt()} грн")
        else:
            print("Перевищено ліміт рахунку.")

    def pay(self, customer_id, amount):
        bill = self._get_bill(customer_id)
        if not bill:
            print("Рахунок не знайдено")
            return
        bill.pay(amount)
        print(f"Оплачено {amount} грн. Залишок боргу: {bill.get_debt()} грн")

    def get_debt(self, customer_id):
        bill = self._get_bill(customer_id)
        return bill.get_debt() if bill else None

def main():
    operators = [
        Operator(1, "Lvivstar", 1.5, 0.5, 0.2),
        Operator(2, "Sikfone", 1.0, 0.7, 0.3),
        Operator(3, "Deathcell", 1.2, 0.6, 0.25)
    ]

    name = input("Введіть ім'я клієнта: ")
    age = int(input("Введіть вік клієнта: "))
    for op in operators:
        print(f"{op.id}. {op.name}")
    op_id = int(input("Оберіть оператора: "))

    customer = Customer(1, name, age, op_id)
    chosen_operator = operators[op_id - 1]
    chosen_operator.create_bill(customer.id)

    while True:
        print("\n1. Дзвінок")
        print("2. Повідомлення")
        print("3. Інтернет")
        print("4. Поповнити рахунок")
        print("5. Перевірити борг")
        print("6. Вийти")
        choice = input("Ваш вибір: ")

        if choice == '1':
            minutes = int(input("Хвилини: "))
            chosen_operator.provide_talk(customer.id, minutes)
        elif choice == '2':
            qty = int(input("Кількість SMS: "))
            chosen_operator.provide_message(customer.id, qty)
        elif choice == '3':
            mb = int(input("МБ: "))
            chosen_operator.provide_internet(customer.id, mb)
        elif choice == '4':
            amount = float(input("Сума: "))
            chosen_operator.pay(customer.id, amount)
        elif choice == '5':
            debt = chosen_operator.get_debt(customer.id)
            print(f"Борг: {debt} грн")
        elif choice == '6':
            break

if __name__ == "__main__":
    main()