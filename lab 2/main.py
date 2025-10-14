import json
import os
from models.port import Port
from models.ship import Ship
from models.container import (
    BasicContainer, HeavyContainer,
    RefrigeratedContainer, LiquidContainer
)

def load_input(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_output(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def create_container(container_data):
    cid = container_data['id']
    weight = container_data['weight']
    ctype = container_data.get('type', None)

    if ctype == 'R':
        return RefrigeratedContainer(cid, weight)
    elif ctype == 'L':
        return LiquidContainer(cid, weight)
    elif weight <= 3000:
        return BasicContainer(cid, weight)
    else:
        return HeavyContainer(cid, weight)

def main(input_file, output_file):
    data = load_input(input_file)

    ports = {p['id']: Port(p['id'], p['latitude'], p['longitude']) for p in data['ports']}
    containers = {c['id']: create_container(c) for c in data['containers']}
    ships = {}

    for s in data['ships']:
        port = ports[s['current_port']]
        ship = Ship(
            s['id'], port, s['fuel'], s['total_weight_capacity'],
            s['max_all'], s['max_heavy'], s['max_refrigerated'],
            s['max_liquid'], s['fuel_per_km']
        )
        port.incoming_ship(ship)
        ships[s['id']] = ship

    for act in data['actions']:
        t = act['type']
        if t == 'refuel':
            ships[act['ship_id']].refuel(act['amount'])
        elif t == 'load':
            ship = ships[act['ship_id']]
            cont = containers[act['container_id']]
            ship.load(cont)
        elif t == 'unload':
            ship = ships[act['ship_id']]
            cont = containers[act['container_id']]
            ship.unload(cont)
        elif t == 'sail':
            ship = ships[act['ship_id']]
            dest = ports[act['to_port']]
            ship.sail_to(dest)

    output = {
        "ports": {
            f"port_{p.id}": {
                "lat": round(p.latitude, 2),
                "lon": round(p.longitude, 2),
                "containers": [c.id for c in sorted(p.containers, key=lambda x: x.id)],
                "ships": {
                    f"ship_{s.id}": {
                        "fuel_left": round(s.fuel, 2),
                        "containers": [c.id for c in sorted(s.containers, key=lambda x: x.id)]
                    } for s in sorted(p.current, key=lambda x: x.id)
                }
            } for p in sorted(ports.values(), key=lambda x: x.id)
        }
    }

    save_output(output, output_file)
    print(f"Simulation complete. Output saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        input_file = os.path.join(data_dir, "input.json")
        output_file = os.path.join(data_dir, "output.json")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    main(input_file, output_file)
