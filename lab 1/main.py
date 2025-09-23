from customer import Customer
from operators import Operator
from bill import Bill

def main():
    # Оператори
    operators = [
        Operator(0, "Київстар", 1.5, 0.5, 0.2, 0.2),
        Operator(1, "Vodafone", 1.0, 0.7, 0.3, 0.15),
        Operator(2, "Lifecell", 1.2, 0.6, 0.25, 0.1)
    ]

    print("Доброго дня! Створимо вашого клієнта.")
    name = input("Введіть ім'я клієнта: ")
    age = int(input("Введіть вік клієнта: "))

    print("Оберіть оператора:")
    for op in operators:
        print(f"{op.id}. {op.name}")
    operator_id = int(input("Введіть номер оператора: "))

    bill = Bill(100)  
    customer = Customer(0, name, age, operators[operator_id], bill)

   
    customer2 = Customer(1, "Влад" , 30, operators[1], Bill(150))

    while True:
        print("\nОберіть дію:")
        print("1. Зателефонувати іншому клієнту")
        print("2. Відправити повідомлення іншому клієнту")
        print("3. Використати інтернет")
        print("4. Сплатити рахунок")
        print("5. Перевірити борг")
        print("6. Змінити оператора")
        print("7. Змінити ліміт рахунку")
        print("8. Вийти")

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
            customer.changeOperator(operators[new_id])
        elif choice == '7':
            new_limit = float(input("Введіть новий ліміт: "))
            customer.changeBillLimit(new_limit)
        elif choice == '8':
            print("До побачення!")
            break
        else:
            print("Невірний вибір!")

if __name__ == "__main__":
    main()
