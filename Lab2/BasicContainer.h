#ifndef BASICCONTAINER_H
#define BASICCONTAINER_H

#include "Container.h"

class BasicContainer : public Container {
public:
    BasicContainer(int id, int w);
    double consumption() const override;
    std::string getTypeName() const override;
};

#endif // BASICCONTAINER_H
