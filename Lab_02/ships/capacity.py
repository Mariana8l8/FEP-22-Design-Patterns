from dataclasses import dataclass

@dataclass
class ShipCapacity:
    total_weight_capacity: int = 0
    max_all: int = 0
    max_basic: int = 0
    max_heavy: int = 0
    max_refrig: int = 0
    max_liquid: int = 0
