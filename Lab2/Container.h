#ifndef CONTAINER_H
#define CONTAINER_H

#include <string>

class Container {
public:
    int ID;
    int weight;
    Container(int id, int w);
    virtual double consumption() const = 0;
    virtual std::string getTypeName() const = 0;
    virtual bool equals(const Container* other) const;
    virtual ~Container() = default;
};

#endif