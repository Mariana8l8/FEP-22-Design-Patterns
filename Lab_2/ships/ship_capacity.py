from dataclasses import dataclass


@dataclass
class ShipCapacity:
    max_weight: int
    max_all: int
    max_basic: int
    max_heavy: int
    max_refrigerated: int
    max_liquid: int

    def to_dict(self) -> dict:
        return {
            "max_weight": self.max_weight,
            "max_all": self.max_all,
            "max_basic": self.max_basic,
            "max_heavy": self.max_heavy,
            "max_refrigerated": self.max_refrigerated,
            "max_liquid": self.max_liquid,
        }
