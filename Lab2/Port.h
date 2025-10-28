#ifndef PORT_H
#define PORT_H

#include "IPort.h"
#include <vector>

class Container;
class Ship;

class Port : public IPort {
public:
    int ID;
    double latitude;
    double longitude;
    std::vector<Container*> containers;
    std::vector<Ship*> history;
    std::vector<Ship*> current;

    Port(int id, double lat, double lon);
    void incomingShip(Ship* s) override;
    void outgoingShip(Ship* s) override;
    double getDistance(Port* other); 
};

#endif
