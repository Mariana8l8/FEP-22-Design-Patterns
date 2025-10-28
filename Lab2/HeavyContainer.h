#ifndef HEAVYCONTAINER_H
#define HEAVYCONTAINER_H

#include "Container.h"

class HeavyContainer : public Container {
public:
    HeavyContainer(int id, int w);
    double consumption() const override;
    std::string getTypeName() const override;
};

#endif
