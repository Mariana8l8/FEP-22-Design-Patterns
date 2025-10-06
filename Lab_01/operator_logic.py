from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from customer_logic import Customer


class Operator:

    operators: dict[int, "Operator"] = {}

    __slots__ = ("_id", "_name", "_talking", "_message", "_network", "_discount")

    def __init__(
        self,
        name: str,
        talkingCharge: float | int,
        messageCost: float | int,
        networkCharge: float | int,
        discountRate: int,
    ) -> None:
        self._name = str(name)
        self._talking = float(talkingCharge)
        self._message = float(messageCost)
        self._network = float(networkCharge)
        self._discount = int(discountRate)

        if self._talking < 0 or self._message < 0 or self._network < 0:
            raise ValueError("Charges must be non-negative")
        if not (0 <= self._discount <= 100):
            raise ValueError("discountRate must be in [0, 100]")

        self._id = (max(Operator.operators) + 1) if Operator.operators else 1
        Operator.operators[self._id] = self

    @property
    def ID(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def talkingCharge(self) -> float:
        return self._talking

    @property
    def messageCost(self) -> float:
        return self._message

    @property
    def networkCharge(self) -> float:
        return self._network

    @property
    def discountRate(self) -> int:
        return self._discount

    def _apply_discount(self, amount: float, same_network: bool) -> float:
        return amount * (100 - self._discount) / 100 if same_network else amount

    def calculate_talking_cost(self, minute: int, customer2: "Customer", operator_id: int) -> float:
        base = minute * self._talking
        same = operator_id in customer2.operator
        return self._apply_discount(base, same)

    def calculate_message_cost(self, quantity: int, customer2: "Customer", operator_id: int) -> float:
        base = quantity * self._message
        same = operator_id in customer2.operator
        return self._apply_discount(base, same)

    def calculate_connection_cost(self, amount: float) -> float:
        return amount * self._network
