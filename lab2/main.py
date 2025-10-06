import json
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from ship import Ship
from port import Port

# 1️⃣ Читання JSON
with open("input.json", "r") as f:
    data = json.load(f)

# 2️⃣ Створюємо порти
ports = {p["ID"]: Port(p["ID"], p["latitude"], p["longitude"]) for p in data["ports"]}

# 3️⃣ Створюємо кораблі
ships = {}
for s in data["ships"]:
    currentPort = ports[s["currentPortID"]]
    ship = Ship(
        ID=s["ID"],
        fuel=s["fuel"],
        totalWeightCapacity=s["totalWeightCapacity"],
        maxNumberOfAllContainers=s["maxNumberOfAllContainers"],
        maxNumberOfHeavyContainers=s["maxNumberOfHeavyContainers"],
        maxNumberOfRefrigeratedContainers=s["maxNumberOfRefrigeratedContainers"],
        maxNumberOfLiquidContainers=s["maxNumberOfLiquidContainers"],
        fuelConsumptionPerKM=s["fuelConsumptionPerKM"],
        currentPort=currentPort
    )
    ships[s["ID"]] = ship
    currentPort.incomingShip(ship)

# 4️⃣ Створюємо контейнери та кладемо у порти
containers = {}
for c in data["containers"]:
    if c["type"] == "Basic":
        container = BasicContainer(c["ID"], c["weight"])
    elif c["type"] == "Heavy":
        container = HeavyContainer(c["ID"], c["weight"])
    elif c["type"] == "Refrigerated":
        container = RefrigeratedContainer(c["ID"], c["weight"])
    elif c["type"] == "Liquid":
        container = LiquidContainer(c["ID"], c["weight"])
    else:
        continue
    containers[c["ID"]] = container
    ports[c["portID"]].containers.append(container)

# 5️⃣ Виконуємо дії
for act in data["actions"]:
    ship = ships[act["shipID"]]
    if act["action"] == "load":
        container = containers[act["containerID"]]
        ship.load(container)
    elif act["action"] == "unload":
        container = containers[act["containerID"]]
        ship.unLoad(container)
        ship.currentPort.containers.append(container)
    elif act["action"] == "sail":
        destination = ports[act["destinationPortID"]]
        ship.sailTo(destination)
    elif act["action"] == "refuel":
        ship.reFuel(act["fuelAmount"])

# 6️⃣ Вивід результату (приклад)
for port in ports.values():
    print(f"Port {port.ID}:")
    print(f"  Containers: {[c.ID for c in port.containers]}")
    for ship in port.current:
        print(f"  Ship {ship.ID} fuel left: {ship.fuel}")
        print(f"    Onboard containers: {[c.ID for c in ship.containers]}")
