from operator import Operator
from customer import Customer

op1 = Operator("Kyivstar", talkingCharge=2.0, messageCost=0.5, networkCharge=0.1, discountRate=10)
op2 = Operator("Vodafone", talkingCharge=3.0, messageCost=0.75, networkCharge=0.15, discountRate=15)
person1 = Customer('Oleg', 18)
person2 = Customer('Danko', 19)
person3 = Customer('Denis', 18)

print("\n=== Підключення операторів ===")
person1.connect_operator(op1)
person2.connect_operator(op2)
person3.connect_operator(op1)

print("\n=== Дзвінки ===")
person1.talk(10, person3)
person1.talk(50, person2)

print("\n=== Повідомлення ===")
person2.message(5, person3)
person3.message(10, person1)

print("\n=== Інтернет ===")
person1.connection(200)
person2.connection(800)

print("\n=== Борг ===")
person1.check_debt()
person2.check_debt()
person3.check_debt()

print("\n=== Оплата ===")
person2.pay(10)
person2.check_debt()

print("\n=== Відключення операторів ===")
person1.disconnect_operator()
person2.disconnect_operator()
person3.disconnect_operator()

print("\n=== Перевірка без оператора ===")
person1.talk(5, person2)

print("\n=== Борг ===")
person1.check_debt()
person2.check_debt()
person3.check_debt()