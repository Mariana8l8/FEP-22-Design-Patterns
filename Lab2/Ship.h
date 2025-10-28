#ifndef SHIP_H
#define SHIP_H

#include "IShip.h"
#include <vector>

class Port;
class Container;

class Ship : public IShip {
public:
    int ID;
    double fuel;
    Port* currentPort;
    int totalWeightCapacity;
    int maxNumberOfAllContainers;
    int maxNumberOfHeavyContainers;
    int maxNumberOfRefrigeratedContainers;
    int maxNumberOfLiquidContainers;
    double fuelConsumptionPerKM;
    std::vector<Container*> onboard;

    Ship(int id, Port* startPort, int maxWeight, int maxAll, int maxHeavy, int maxRefrig, int maxLiquid, double fuelPerKm);

    std::vector<Container*> getCurrentContainers();

    bool sailTo(Port* p) override;
    void reFuel(double newFuel) override;
    bool load(Container* cont) override;
    bool unLoad(Container* cont) override;
};

#endif
