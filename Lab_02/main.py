import json
import os

from ports.port import Port
from container.container import (
    BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
)
from ships.ship import Ship
from ships.capacity import ShipCapacity


def print_port_containers(title: str, port: Port) -> None:
    print()
    print(title)
    if not port.containers:
        print("немає контейнерів")
        return
    for cid in sorted(port.containers):
        c = port.containers[cid]
        print(f"ID={c.ID:02d} | {type(c).__name__:<18} | weight={c.weight}")
    print()


def load_data(filename: str = "ports_data.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def needed_fuel(ship: Ship, from_port: Port, to_port: Port) -> float:
    distance = from_port.getDistance(to_port)
    containers_consumption = sum(c.consumption() for c in ship.getCurrentContainers())
    return (ship.fuelPerKm + containers_consumption) * distance


def main():
    data = load_data("ports_data.json")

    # 1) Порти
    port1 = Port(data["Port_1"]["lat"], data["Port_1"]["lon"])
    port2 = Port(data["Port_2"]["lat"], data["Port_2"]["lon"])

    # [Тест] Кладемо кілька контейнерів у Порт 1
    test_containers = [
        BasicContainer(800),
        HeavyContainer(1200),
        RefrigeratedContainer(600),
        LiquidContainer(700),
    ]
    for c in test_containers:
        port1.put_container(c)

    # (а) Друк стану Порту 1
    print_port_containers("Контейнери у Порті 1 (перед відправленням)", port1)

    # 2) Беремо перший корабель із JSON (наприклад, ship_1)
    ship_key = next(k for k in data["Port_2"] if k.startswith("ship_"))
    ship_info = data["Port_2"][ship_key]

    capacity = ShipCapacity(
        total_weight_capacity=ship_info["max_weight"],
        max_all=ship_info["max_all"],
        max_basic=ship_info["max_all"],
        max_heavy=ship_info["max_all"],
        max_refrig=ship_info["max_all"],
        max_liquid=ship_info["max_all"]
    )

    ship = Ship(currentPort=port1, capacity=capacity, fuelPerKm=0.1)
    ship.reFuel(ship_info["fuel"])

    # (б) Завантажуємо УСІ контейнери з Порту 1
    for cid in list(sorted(port1.containers.keys())):
        ship.load(cid)

    # 3) Дозаправка рівно під рейс (з невеликим запасом)
    req = needed_fuel(ship, port1, port2)
    need_with_margin = req * 1.05
    if ship.fuel < need_with_margin:
        ship.reFuel(need_with_margin - ship.fuel)

    print("Вирушаємо до Порту 2")

    # 4) Перехід і вигрузка
    if not ship.sailTo(port2):
        print("Не вдалося вирушити")
        return

    for c in ship.getCurrentContainers():
        ship.unLoad(c.ID)

    # (в) Друк стану Порту 2 після прибуття
    print_port_containers("Контейнери у Порті 2 (після прибуття)", port2)


if __name__ == "__main__":
    main()
