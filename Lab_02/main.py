import json
import os
from pprint import pprint

from ports.port import Port
from container.container import (
    BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
)
from ships.ship import Ship
from ships.capacity import ShipCapacity

def load_data(filename: str = "ports_data.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_port(port_data: dict) -> Port:
    return Port(port_data["lat"], port_data["lon"])


def add_containers_from_lists(port: Port, data_port: dict) -> None:
    for w in data_port.get("basic_container", []):
        port.put_container(BasicContainer(int(w)))
    for w in data_port.get("heavy_container", []):
        port.put_container(HeavyContainer(int(w)))
    for w in data_port.get("refrigerated_container", []):
        port.put_container(RefrigeratedContainer(int(w)))
    for w in data_port.get("liquid_container", []):
        port.put_container(LiquidContainer(int(w)))

def ship_block_dict(ship: Ship, cap: ShipCapacity) -> dict:
    return {
        "fuel": round(ship.fuel, 2),
        "fuel_consumption_per_km": ship.fuelPerKm,
        "max_weight": cap.total_weight_capacity,
        "max_all": cap.max_all,
        "max_basic": cap.max_basic,
        "max_heavy": cap.max_heavy,
        "max_refrigerated": cap.max_refrig,
        "max_liquid": cap.max_liquid,
        "basic_container": [],
        "heavy_container": [],
        "refrigerated_container": [],
        "liquid_container": [],
    }


def _typed_id_lists(port: Port) -> dict:
    basic, heavy, refr, liq = [], [], [], []
    for _, c in port.containers.items():
        if isinstance(c, BasicContainer):
            basic.append(c.ID)
        elif isinstance(c, HeavyContainer):
            heavy.append(c.ID)
        elif isinstance(c, RefrigeratedContainer):
            refr.append(c.ID)
        elif isinstance(c, LiquidContainer):
            liq.append(c.ID)
    return {
        "basic_container": sorted(basic),
        "heavy_container": sorted(heavy),
        "refrigerated_container": sorted(refr),
        "liquid_container": sorted(liq),
        "lat": port.latitude,
        "lon": port.longitude,
    }


def snapshot_ports_dict(port1: Port, port2: Port, ship: Ship | None = None, cap: ShipCapacity | None = None) -> dict:
    snap = {
        "Port_1": _typed_id_lists(port1),
        "Port_2": _typed_id_lists(port2),
    }
    if ship is not None and cap is not None:
        block = ship_block_dict(ship, cap)
        if ship.currentPort is port1:
            snap["Port_1"]["ship_1"] = block
        elif ship.currentPort is port2:
            snap["Port_2"]["ship_1"] = block
    return snap


def needed_fuel(ship: Ship, from_port: Port, to_port: Port) -> float:
    distance = from_port.getDistance(to_port)
    containers_consumption = sum(c.consumption() for c in ship.getCurrentContainers())
    return (ship.fuelPerKm + containers_consumption) * distance


def main():
    data = load_data("ports_data.json")

    port1 = build_port(data["Port_1"])
    port2 = build_port(data["Port_2"])

    add_containers_from_lists(port1, data["Port_1"])
    add_containers_from_lists(port2, data["Port_2"])

    ship_cfg = data["Port_1"]["ship_1"]
    capacity = ShipCapacity(
        total_weight_capacity=ship_cfg["max_weight"],
        max_all=ship_cfg["max_all"],
        max_basic=ship_cfg["max_basic"],
        max_heavy=ship_cfg["max_heavy"],
        max_refrig=ship_cfg["max_refrigerated"],
        max_liquid=ship_cfg["max_liquid"],
    )
    ship = Ship(currentPort=port1, capacity=capacity, fuelPerKm=ship_cfg["fuel_consumption_per_km"])
    ship.reFuel(ship_cfg["fuel"])

    print("\n=== Стан портів перед рейсом ===")
    pprint(snapshot_ports_dict(port1, port2, ship, capacity))

    for cid in list(sorted(port1.containers.keys())):
        ship.load(cid)

    req = needed_fuel(ship, port1, port2)
    if ship.fuel < req:
        ship.reFuel(req - ship.fuel)
    print("\nShip_1 refueled with enough fuel to reach the destination.\n")

    if not ship.sailTo(port2):
        print("❌ Sailing failed (check fuel/limits).")
        return

    for c in ship.getCurrentContainers():
        ship.unLoad(c.ID)

    print("\n=== Стан портів після прибуття ===")
    pprint(snapshot_ports_dict(port1, port2, ship, capacity))


if __name__ == "__main__":
    main()
