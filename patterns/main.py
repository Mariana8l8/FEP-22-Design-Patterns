from customer import Customer, Customer2
from operators import Operator
from bill import Bill

def main():
    # Оператори
    operators = [
        Operator(1, "Київстар", 1.5, 0.5, 0.2, 0.2),
        Operator(2, "Vodafone", 1.0, 0.7, 0.3, 0.15),
        Operator(3, "Lifecell", 1.2, 0.6, 0.25, 0.1)
    ]

    print("Доброго дня! Створимо ваших клієнтів.")
    name = input("Введіть ім'я клієнта: ")
    age = int(input("Введіть вік клієнта: "))
    name2 = input("Введіть ім'я другого клієнта: ")
    age2 = int(input("Введіть вік другого клієнта: "))

    print("Оберіть операторів:")
    for op in operators:
        print(f"{op.id}. {op.name}")
    operator_id = int(input("Введіть номер оператора: "))
    operator_id2 = int(input("Введіть номер оператора для другого клієнта: "))

    bill = Bill(250)  
    bill2 = Bill(175)
    customer = Customer(0, name, age, operators[operator_id], bill)
    customer2 = Customer2(1, name2, age2, operators[operator_id2], bill2)

    while True:
        print("\nОберіть дію:")
        print("1. Зателефонувати іншому клієнту (1 -> 2)")
        print("2. Відправити повідомлення іншому клієнту (1 -> 2)")
        print("3. Використати інтернет (1)")
        print("4. Сплатити рахунок (1)")
        print("5. Перевірити борг (1)")
        print("6. Змінити оператора (1)")
        print("7. Змінити ліміт рахунку (1)")
        print("8. Зателефонувати іншому клієнту (2 -> 1)")
        print("9. Відправити повідомлення іншому клієнту (2 -> 1)")
        print("10. Використати інтернет (2)")
        print("11. Сплатити рахунок (2)")
        print("12. Перевірити борг (2)")
        print("13. Змінити оператора (2)")
        print("14. Змінити ліміт рахунку (2)")
        print("15. Вийти")

        choice = input("Ваш вибір: ")

        if choice == '1':
            minutes = int(input("Введіть кількість хвилин: "))
            customer.talk(minutes, customer2)
        elif choice == '2':
            qty = int(input("Введіть кількість повідомлень: "))
            customer.message(qty, customer2)
        elif choice == '3':
            mb = float(input("Введіть кількість МБ: "))
            customer.connection(mb)
        elif choice == '4':
            amount = float(input("Введіть суму для оплати: "))
            customer.payBill(amount)
        elif choice == '5':
            print(f"Ваш борг: {bill.getCurrentDebt():.2f} грн, ліміт: {bill.getLimitingAmount()} грн")
        elif choice == '6':
            print("Оберіть нового оператора:")
            for op in operators:
                print(f"{op.id}. {op.name}")
            new_id = int(input("Введіть номер: "))
            customer.changeOperator(operators[new_id - 1])
        elif choice == '7':
            new_limit = float(input("Введіть новий ліміт: "))
            customer.changeBillLimit(new_limit)
        elif choice == '8':
            minutes = int(input("Введіть кількість хвилин: "))
            customer2.talk(minutes, customer)
        elif choice == '9':
            qty = int(input("Введіть кількість повідомлень: "))
            customer2.message(qty, customer)
        elif choice == '10':
            mb = float(input("Введіть кількість МБ: "))
            customer2.connection(mb)
        elif choice == '11':
            amount = float(input("Введіть суму для оплати: "))
            customer2.payBill(amount)
        elif choice == '12':
            print(f"Ваш борг: {bill2.getCurrentDebt():.2f} грн, ліміт: {bill2.getLimitingAmount()} грн")
        elif choice == '13':
            print("Оберіть нового оператора:")
            for op in operators:
                print(f"{op.id}. {op.name}")
            new_id = int(input("Введіть номер: "))
            customer2.changeOperator(operators[new_id - 1])
        elif choice == '14':
            new_limit = float(input("Введіть новий ліміт: "))
            customer2.changeBillLimit(new_limit)
        elif choice == '15':
            break
        else:
            print("Невірний вибір!")

if __name__ == "__main__":
    main()