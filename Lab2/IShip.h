#ifndef ISHIP_H
#define ISHIP_H

class Port;
class Container;

class IShip {
public:
    virtual bool sailTo(Port* p) = 0;
    virtual void reFuel(double newFuel) = 0;
    virtual bool load(Container* cont) = 0;
    virtual bool unLoad(Container* cont) = 0;
    virtual ~IShip() = default;
};

#endif
