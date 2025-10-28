#ifndef LIQUIDCONTAINER_H
#define LIQUIDCONTAINER_H

#include "HeavyContainer.h"

class LiquidContainer : public HeavyContainer {
public:
    LiquidContainer(int id, int w);
    double consumption() const override;
    std::string getTypeName() const override;
};

#endif // LIQUIDCONTAINER_H
