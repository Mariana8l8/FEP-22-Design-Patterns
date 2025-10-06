from utils import check_amount
from bill import Bill
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from operator_logic import Operator

class Customer:
    customers: dict[int, 'Customer'] = {}

    def __init__(self, name: str, age: int):
        self.__name: str = str(name)
        self.__age: int = int(age)
        self.__operator: dict[int, 'Operator'] = {}
        self.__bills: dict[int, Bill] = {}

        if Customer.customers:
            self.__ID: int = max(Customer.customers.keys()) + 1
        else:
            self.__ID: int = 1
        Customer.customers[self.__ID] = self

    @property
    def ID(self): return self.__ID
    @property
    def name(self): return self.__name
    @property
    def age(self): return self.__age
    @property
    def operator(self): return self.__operator
    @property
    def bills(self): return self.__bills

    def _has_op_and_units(self, units: float, operator_id: int) -> bool:
        if operator_id not in self.__operator:
            print(f"{self.__name} is not connected to operator {operator_id}.")
            return False
        if check_amount(units):
            return False
        if operator_id not in self.__bills:
            print(f"No bill linked for operator {operator_id} on {self.__name}.")
            return False
        return True

    def talk(self, minute: int, customer: 'Customer', operator_id: int):
        if not self._has_op_and_units(minute, operator_id): return
        if not customer.operator:
            print(f"{customer.name} does not have an operator assigned."); return
        op = self.__operator[operator_id]; bill = self.__bills[operator_id]
        total = op.calculate_talking_cost(minute, customer, operator_id)
        left = bill.limitingAmount - bill.currentDebt; per = op.talkingCharge
        if total <= left:
            bill.add(total); print(f"{self.name} talked with {customer.name} for {minute} minutes. Cost: {total:.2f}")
        elif left == 0:
            print(f"{self.name} cannot make a call; credit limit reached ({bill.currentDebt:.2f}/{bill.limitingAmount:.2f}).")
        else:
            max_m = int(left // per); bill.add(left)
            print(f"{self.name}'s call with {customer.name} was cut after {max_m} minutes. Limit reached ({bill.limitingAmount:.2f}).")

    def message(self, qty: int, customer: 'Customer', operator_id: int):
        if not self._has_op_and_units(qty, operator_id): return
        if not customer.operator:
            print(f"{customer.name} does not have an operator assigned."); return
        op = self.__operator[operator_id]; bill = self.__bills[operator_id]
        total = op.calculate_message_cost(qty, customer, operator_id)
        left = bill.limitingAmount - bill.currentDebt; per = op.messageCost
        if total <= left:
            bill.add(total); print(f"{self.name} sent {qty} messages to {customer.name}. Cost: {total:.2f}")
        elif left == 0:
            print(f"{self.name} cannot send messages; credit limit reached ({bill.currentDebt:.2f}/{bill.limitingAmount:.2f}).")
        else:
            max_q = int(left // per); bill.add(left)
            print(f"{self.name} could only send {max_q} messages to {customer.name}. Limit reached ({bill.limitingAmount:.2f}).")

    def connection(self, mb: float, operator_id: int):
        if not self._has_op_and_units(mb, operator_id): return
        op = self.__operator[operator_id]; bill = self.__bills[operator_id]
        total = op.calculate_connection_cost(mb)
        left = bill.limitingAmount - bill.currentDebt
        if total <= left:
            bill.add(total); print(f"{self.name} used {mb:.2f} MB. Cost: {total:.2f}")
        elif left == 0:
            print(f"{self.name} cannot use internet; credit limit reached ({bill.currentDebt:.2f}/{bill.limitingAmount:.2f}).")
        else:
            max_mb = left / op.networkCharge; bill.add(left)
            print(f"{self.name} could only use {max_mb:.2f} MB. Limit reached ({bill.limitingAmount:.2f}).")

    def check_debt(self, operator_id: int | None = None):
        if operator_id is None:
            if not self.__bills: print(f"{self.name} has no bills."); return
            for oid, b in self.__bills.items():
                print(f"{self.name} — operator {oid}: debt {b.currentDebt:.2f}, limit {b.limitingAmount:.2f}")
        else:
            if operator_id not in self.__bills:
                print(f"No bill for operator {operator_id} on {self.__name}."); return
            b = self.__bills[operator_id]
            print(f"{self.name} — operator {operator_id}: debt {b.currentDebt:.2f}, limit {b.limitingAmount:.2f}")

    def pay(self, amount: float, operator_id: int):
        if check_amount(amount): return
        if operator_id not in self.__bills:
            print(f"No bill for operator {operator_id} on {self.__name}."); return
        b = self.__bills[operator_id]; b.pay(amount)
        print(f"{self.name} paid {amount:.2f} for operator {operator_id}. Current debt: {b.currentDebt:.2f}, limit: {b.limitingAmount:.2f}")

    def connect_operator(self, operator: 'Operator'):
        self.__operator[operator.ID] = operator
        typical_m, typical_sms, typical_mb = 120, 100, 2000
        limit = operator.talkingCharge * typical_m + operator.messageCost * typical_sms + operator.networkCharge * typical_mb
        self.__bills[operator.ID] = Bill(limitingAmount=limit, currentDebt=0.0)
        print(f"{self.__name} connected to operator {operator.ID}. Limiting amount set to {limit:.2f}.")

    def disconnect_operator(self, operator_id: int):
        if operator_id not in self.__operator:
            print(f"{self.__name} is not connected to operator {operator_id}."); return
        op_name = self.__operator.pop(operator_id).name
        self.__bills.pop(operator_id, None)
        print(f"{self.__name} has disconnected from operator {op_name}. Bill removed.")
