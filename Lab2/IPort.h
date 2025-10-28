#ifndef IPORT_H
#define IPORT_H

class Ship;

class IPort {
public:
    virtual void incomingShip(Ship* s) = 0;
    virtual void outgoingShip(Ship* s) = 0;
    virtual ~IPort() = default;
};

#endif
