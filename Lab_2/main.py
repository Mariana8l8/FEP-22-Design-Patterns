import json
from pprint import pprint
from containers.basic import BasicContainer
from containers.heavy import HeavyContainer
from containers.liquid import LiquidContainer
from containers.refrigerated import RefrigeratedContainer
from ports.port import Port
from ships.ship import Ship
from ships.ship_capacity import ShipCapacity

port1 = Port(latitude=50.45, longitude=30.52)
port2 = Port(latitude=48.85, longitude=2.35)

capacity1 = ShipCapacity(max_weight=10000, max_all=5, max_basic=2, max_heavy=2, max_refrigerated=1, max_liquid=1)
capacity2 = ShipCapacity(max_weight=15000, max_all=6, max_basic=3, max_heavy=2, max_refrigerated=1, max_liquid=2)

ship1 = Ship(fuel=5000.0, port=port1, fuel_consumption_per_km=10.0, capacity=capacity1)
ship2 = Ship(fuel=8000.0, port=port1, fuel_consumption_per_km=12.0, capacity=capacity2)

basic1 = BasicContainer(weight=2000)
basic2 = BasicContainer(weight=2500)
heavy1 = HeavyContainer(weight=4000)
refrigerated1 = RefrigeratedContainer(weight=5000)
liquid1 = LiquidContainer(weight=4500)

port1.load_container(basic1)
port1.load_container(basic2)
port1.load_container(heavy1)
port1.load_container(refrigerated1)
port1.load_container(liquid1)

ship1.load(basic1)
ship1.load(heavy1)

ship2.load(basic2)
ship2.load(refrigerated1)
ship2.load(liquid1)

pprint({
    **port1.to_dict(),
    **port2.to_dict(),
})

ship1.sail_to(port2)
ship2.sail_to(port2)

ship1.unload(basic1.id)
ship1.unload(heavy1.id)

ship2.unload(refrigerated1.id)
ship2.unload(liquid1.id)

ports_data = {
    **port1.to_dict(),
    **port2.to_dict(),
}

pprint(ports_data)

with open("ports_data.json", "w", encoding="utf-8") as f:
    json.dump(ports_data, f, ensure_ascii=False, indent=4)
