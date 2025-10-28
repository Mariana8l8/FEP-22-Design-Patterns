
#include <bits/stdc++.h>
#include "json.hpp"
using json = nlohmann::json;
using namespace std;

#include "IPort.h"
#include "IShip.h"
#include "Container.h"
#include "BasicContainer.h"
#include "HeavyContainer.h"
#include "RefrigeratedContainer.h"
#include "LiquidContainer.h"
#include "Port.h"
#include "Ship.h"
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

Container::Container(int id, int w) : ID(id), weight(w) {}
bool Container::equals(const Container* other) const {
    if (!other) return false;
    return (ID == other->ID) && (weight == other->weight) && (getTypeName() == other->getTypeName());
}

BasicContainer::BasicContainer(int id, int w): Container(id,w){}
double BasicContainer::consumption() const { return 2.5 * weight; }
string BasicContainer::getTypeName() const { return "BasicContainer"; }

HeavyContainer::HeavyContainer(int id, int w): Container(id,w){}
double HeavyContainer::consumption() const { return 3.0 * weight; }
string HeavyContainer::getTypeName() const { return "HeavyContainer"; }

RefrigeratedContainer::RefrigeratedContainer(int id,int w): HeavyContainer(id,w){}
double RefrigeratedContainer::consumption() const { return 5.0 * weight; }
string RefrigeratedContainer::getTypeName() const { return "RefrigeratedContainer"; }

LiquidContainer::LiquidContainer(int id,int w): HeavyContainer(id,w){}
double LiquidContainer::consumption() const { return 4.0 * weight; }
string LiquidContainer::getTypeName() const { return "LiquidContainer"; }

Port::Port(int id, double lat, double lon) : ID(id), latitude(lat), longitude(lon) {}
void Port::incomingShip(Ship* s) {
    if (!s) return;
    if (find(current.begin(), current.end(), s) == current.end()) current.push_back(s);
    bool inHist = false;
    for (auto sh : history) if (sh == s) { inHist = true; break; }
    if (!inHist) history.push_back(s);
}
void Port::outgoingShip(Ship* s) {
    if (!s) return;
    current.erase(remove(current.begin(), current.end(), s), current.end());
    bool inHist = false;
    for (auto sh : history) if (sh == s) { inHist = true; break; }
    if (!inHist) history.push_back(s);
}
double Port::getDistance(Port* other) {
    if (!other) return 0.0;
    constexpr double R = 6371.0;
    double lat1 = latitude * M_PI/180.0;
    double lat2 = other->latitude * M_PI/180.0;
    double dlat = lat2 - lat1;
    double dlon = (other->longitude - longitude) * M_PI/180.0;
    double a = sin(dlat/2)*sin(dlat/2) + cos(lat1)*cos(lat2)*sin(dlon/2)*sin(dlon/2);
    double c = 2 * atan2(sqrt(a), sqrt(1-a));
    return R * c;
}

Ship::Ship(int id, Port* startPort, int maxWeight, int maxAll, int maxHeavy, int maxRefrig, int maxLiquid, double fuelPerKm)
: ID(id), fuel(0.0), currentPort(startPort), totalWeightCapacity(maxWeight), maxNumberOfAllContainers(maxAll),
  maxNumberOfHeavyContainers(maxHeavy), maxNumberOfRefrigeratedContainers(maxRefrig),
  maxNumberOfLiquidContainers(maxLiquid), fuelConsumptionPerKM(fuelPerKm)
{
    if (currentPort) currentPort->incomingShip(this);
}

vector<Container*> Ship::getCurrentContainers() {
    vector<Container*> copy = onboard;
    sort(copy.begin(), copy.end(), [](Container* a, Container* b){ return a->ID < b->ID; });
    return copy;
}

void Ship::reFuel(double newFuel) {
    if (newFuel <= 0) return;
    fuel += newFuel;
}

bool Ship::load(Container* cont) {
    if (!currentPort || !cont) return false;
    auto it = find(currentPort->containers.begin(), currentPort->containers.end(), cont);
    if (it == currentPort->containers.end()) return false;

    int currentAll = (int)onboard.size();
    if (maxNumberOfAllContainers != 0 && currentAll + 1 > maxNumberOfAllContainers) return false;

    int heavyCount = 0, refrCount = 0, liqCount = 0;
    int currentWeight = 0;
    for (auto c : onboard) {
        currentWeight += c->weight;
        string t = c->getTypeName();
        if (t=="HeavyContainer" || t=="RefrigeratedContainer" || t=="LiquidContainer") heavyCount++;
        if (t=="RefrigeratedContainer") refrCount++;
        if (t=="LiquidContainer") liqCount++;
    }
    if (currentWeight + cont->weight > totalWeightCapacity) return false;

    string tt = cont->getTypeName();
    if ((tt=="HeavyContainer" || tt=="RefrigeratedContainer" || tt=="LiquidContainer")) {
        if (maxNumberOfHeavyContainers != 0 && heavyCount + 1 > maxNumberOfHeavyContainers) return false;
    }
    if (tt=="RefrigeratedContainer") {
        if (maxNumberOfRefrigeratedContainers != 0 && refrCount + 1 > maxNumberOfRefrigeratedContainers) return false;
    }
    if (tt=="LiquidContainer") {
        if (maxNumberOfLiquidContainers != 0 && liqCount + 1 > maxNumberOfLiquidContainers) return false;
    }

    currentPort->containers.erase(remove(currentPort->containers.begin(), currentPort->containers.end(), cont), currentPort->containers.end());
    onboard.push_back(cont);
    return true;
}

bool Ship::unLoad(Container* cont) {
    if (!cont) return false;
    auto it = find(onboard.begin(), onboard.end(), cont);
    if (it == onboard.end()) return false;
    onboard.erase(it);
    if (currentPort) currentPort->containers.push_back(cont);
    return true;
}

bool Ship::sailTo(Port* p) {
    if (!p || !currentPort) return false;
    double dist = currentPort->getDistance(p);
    double need = dist * fuelConsumptionPerKM;
    double contCons = 0.0;
    for (auto c : onboard) contCons += c->consumption();
    double totalNeed = need + contCons;
    if (fuel + 1e-9 < totalNeed) return false;
    fuel -= totalNeed;
    currentPort->outgoingShip(this);
    currentPort = p;
    currentPort->incomingShip(this);
    return true;
}

static unordered_map<int, Port*> ports;
static unordered_map<int, Ship*> ships;
static unordered_map<int, Container*> containers;

Container* makeContainer(int id, int weight, const string& specialType="") {
    if (specialType == "R") return new RefrigeratedContainer(id, weight);
    if (specialType == "L") return new LiquidContainer(id, weight);
    if (weight <= 3000) return new BasicContainer(id, weight);
    return new HeavyContainer(id, weight);
}


json generateOutput() {
    vector<int> portIds;
    for (auto &kv : ports) portIds.push_back(kv.first);
    sort(portIds.begin(), portIds.end());
    json out = json::object();
    for (int pid : portIds) {
        Port* P = ports[pid];
        json portobj = json::object();
        portobj["lat"] = round(P->latitude * 100.0) / 100.0;
        portobj["lon"] = round(P->longitude * 100.0) / 100.0;
        vector<int> basic, heavy, refr, liquid;
        for (auto c : P->containers) {
            string t = c->getTypeName();
            if (t=="BasicContainer") basic.push_back(c->ID);
            else if (t=="HeavyContainer") heavy.push_back(c->ID);
            else if (t=="RefrigeratedContainer") refr.push_back(c->ID);
            else if (t=="LiquidContainer") liquid.push_back(c->ID);
        }
        sort(basic.begin(), basic.end());
        sort(heavy.begin(), heavy.end());
        sort(refr.begin(), refr.end());
        sort(liquid.begin(), liquid.end());
        portobj["basic_container"] = basic;
        portobj["heavy_container"] = heavy;
        portobj["refrigerated_container"] = refr;
        portobj["liquid_container"] = liquid;

        vector<int> shipIds;
        for (auto s : P->current) shipIds.push_back(s->ID);
        sort(shipIds.begin(), shipIds.end());
        for (int sid : shipIds) {
            Ship* S = ships[sid];
            json shipobj = json::object();
            shipobj["fuel_left"] = round(S->fuel * 100.0) / 100.0;
            vector<int> sbasic, sheavy, srefr, sliq;
            for (auto c : S->onboard) {
                string t = c->getTypeName();
                if (t=="BasicContainer") sbasic.push_back(c->ID);
                else if (t=="HeavyContainer") sheavy.push_back(c->ID);
                else if (t=="RefrigeratedContainer") srefr.push_back(c->ID);
                else if (t=="LiquidContainer") sliq.push_back(c->ID);
            }
            sort(sbasic.begin(), sbasic.end());
            sort(sheavy.begin(), sheavy.end());
            sort(srefr.begin(), srefr.end());
            sort(sliq.begin(), sliq.end());
            shipobj["basic_container"] = sbasic;
            shipobj["heavy_container"] = sheavy;
            shipobj["refrigerated_container"] = srefr;
            shipobj["liquid_container"] = sliq;
            string key = "ship_" + to_string(sid);
            portobj[key] = shipobj;
        }
        string portKey = "Port " + to_string(pid);
        out[portKey] = portobj;
    }
    return out;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ifstream ifs("input.json");
    if (!ifs.is_open()) {
        cerr << "Cannot open input.json\n";
        return 1;
    }
    json ops;
    try { ifs >> ops; }
    catch(...) { cerr << "Failed to parse input.json\n"; return 1; }

    for (const auto &op : ops) {
        if (!op.contains("action")) continue;
        string action = op["action"].get<string>();

        if (action == "create_port") {
            int id = op["id"].get<int>();
            double lat = op["lat"].get<double>();
            double lon = op["lon"].get<double>();
            if (ports.find(id) == ports.end()) ports[id] = new Port(id, lat, lon);
        } else if (action == "create_ship") {
            int id = op["id"].get<int>();
            int port_id = op["port_id"].get<int>();
            int maxWeight = op["max_weight"].get<int>();
            int maxAll = op["max_all"].get<int>();
            int maxHeavy = op["max_heavy"].get<int>();
            int maxRefrig = op["max_refrig"].get<int>();
            int maxLiquid = op["max_liquid"].get<int>();
            double fuelPerKm = op["fuelPerKm"].get<double>();
            Port* start = nullptr;
            if (ports.find(port_id) != ports.end()) start = ports[port_id];
            Ship* s = new Ship(id, start, maxWeight, maxAll, maxHeavy, maxRefrig, maxLiquid, fuelPerKm);
            ships[id] = s;
        } else if (action == "create_container") {
            int id = op["id"].get<int>();
            int weight = op["weight"].get<int>();
            string type = "";
            if (op.contains("type")) type = op["type"].get<string>();
            Container* c = makeContainer(id, weight, type);
            containers[id] = c;
            if (op.contains("port_id")) {
                int pid = op["port_id"].get<int>();
                if (ports.find(pid) != ports.end()) ports[pid]->containers.push_back(c);
            }
        } else if (action == "load") {
            int sid = op["ship_id"].get<int>();
            int cid = op["container_id"].get<int>();
            if (ships.find(sid) != ships.end() && containers.find(cid) != containers.end()) {
                ships[sid]->load(containers[cid]);
            }
        } else if (action == "unload") {
            int sid = op["ship_id"].get<int>();
            int cid = op["container_id"].get<int>();
            if (ships.find(sid) != ships.end() && containers.find(cid) != containers.end()) {
                ships[sid]->unLoad(containers[cid]);
            }
        } else if (action == "sail") {
            int sid = op["ship_id"].get<int>();
            int dest = op["dest_port_id"].get<int>();
            if (ships.find(sid) != ships.end() && ports.find(dest) != ports.end()) {
                ships[sid]->sailTo(ports[dest]);
            }
        } else if (action == "refuel" || action == "reFuel") {
            int sid = op["ship_id"].get<int>();
            double f = op["fuel"].get<double>();
            if (ships.find(sid) != ships.end()) ships[sid]->reFuel(f);
        }
    }

    json out = generateOutput();
    ofstream ofs("output.json");
    if (!ofs.is_open()) { cerr << "Cannot open output.json\n"; return 1; }
    ofs << out.dump(4);
    ofs.close();
    return 0;
}
