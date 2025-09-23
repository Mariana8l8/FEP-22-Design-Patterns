from customer import Customer
from operators import Operator
from bill import Bill

def main():
    N = 2  # Кількість клієнтів
    M = 2  # Кількість операторів

    # Створюємо масиви
    customers = [None] * N
    operators = [None] * M
    bills = [None] * N

    # Створення операторів
    operators[0] = Operator(0, 0.5, 0.2, 0.1, 10)
    operators[1] = Operator(1, 0.6, 0.25, 0.15, 15)

    # Створення клієнтів та рахунків
    bills[0] = Bill(50)
    bills[1] = Bill(100)

    customers[0] = Customer(0, "Alice", 17, [operators[0]], [bills[0]], 50)
    customers[1] = Customer(1, "Bob", 30, [operators[1]], [bills[1]], 100)

    # Тестові операції
    customers[0].talk(10, customers[1])
    customers[0].message(5, customers[1])
    customers[1].connection(200)

    customers[0].payBill(20)
    customers[1].changeOperator(operators[0])
    customers[1].changeBillLimit(200)

if __name__ == "__main__":
    main()