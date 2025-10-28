#ifndef REFRIGERATEDCONTAINER_H
#define REFRIGERATEDCONTAINER_H

#include "HeavyContainer.h"

class RefrigeratedContainer : public HeavyContainer {
public:
    RefrigeratedContainer(int id, int w);
    double consumption() const override;
    std::string getTypeName() const override;
};

#endif 
