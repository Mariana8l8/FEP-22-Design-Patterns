#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Bill {
private:
    double limitingAmount;
    double currentDebt;
public:
    Bill(double limit) : limitingAmount(limit), currentDebt(0) {}
    bool check(double amount) { return (currentDebt + amount) <= limitingAmount; }
    void add(double amount) {
        if (check(amount)) currentDebt += amount;
        else cout << "Ліміт перевищено!\n";
    }
    void pay(double amount) { currentDebt = (amount <= currentDebt) ? currentDebt - amount : 0; }
    void changeTheLimit(double amount) { limitingAmount = amount; }
    double getLimitingAmount() { return limitingAmount; }
    double getCurrentDebt() { return currentDebt; }
};

class Operator;

class Customer {
private:
    int ID;
    string name;
    int age;
    vector<Operator*> operators;
    Bill* bill;
public:
    Customer(int id, string n, int a, Operator* o, Bill* b) : ID(id), name(n), age(a), bill(b) {
        if (o != nullptr) addOperator(o);
    }
    void addOperator(Operator* o);
    void removeOperator(Operator* o);
    void talk(Customer& other, int minute);
    void message(Customer& other, int quantity);
    void connection(double amount);
    void payBill(double amount);
    void changeOperator(Operator* newOp);
    void changeBillLimit(double newLimit);
    void showInfo();
    int getAge() { return age; }
    int getID() { return ID; }
    vector<Operator*>& getOperators() { return operators; }
    string getName() { return name; }
};

class Operator {
private:
    int ID;
    double talkingCharge, messageCost, networkCharge;
    int discountRate;
    vector<Customer*> customers;
public:
    Operator(int id, double t, double m, double n, int d)
        : ID(id), talkingCharge(t), messageCost(m), networkCharge(n), discountRate(d) {}

    int getID() { return ID; }
    void addCustomer(Customer* c) {
        for (auto cust : customers)
            if (cust->getID() == c->getID()) return;
        customers.push_back(c);
    }
    void removeCustomer(Customer* c) {
        for (auto it = customers.begin(); it != customers.end(); ++it) {
            if ((*it)->getID() == c->getID()) {
                customers.erase(it);
                return;
            }
        }
    }
    double calculateTalkingCost(int minute, int age) {
        double cost = minute * talkingCharge;
        if (age < 18 || age > 65) cost *= (1 - discountRate / 100.0);
        return cost;
    }
    double calculateMessageCost(int quantity, int op1, int op2) {
        double cost = quantity * messageCost;
        if (op1 == op2) cost *= (1 - discountRate / 100.0);
        return cost;
    }
    double calculateNetworkCost(double amount) { return amount * networkCharge; }
    void showCustomers() {
        cout << "Клієнти оператора ID " << ID << ":\n";
        for (auto customer : customers) {
            customer->showInfo();
        }
    }
};


void Customer::addOperator(Operator* o) {
    if (!o) return;
    for (Operator* op : operators) {
        if (op->getID() == o->getID()) return;
    }
    operators.push_back(o);
    o->addCustomer(this);
}

void Customer::removeOperator(Operator* o) {
    if (!o) return;
    for (auto it = operators.begin(); it != operators.end(); ++it) {
        if ((*it)->getID() == o->getID()) {
            operators.erase(it);
            o->removeCustomer(this);
            return;
        }
    }
}

void Customer::talk(Customer& other, int minute) {
    if (!bill) { cout << name << " не має рахунку.\n"; return; }
    if (operators.empty()) { cout << name << " не має оператора.\n"; return; }
    double cost = 0;

    for (Operator* op : operators) {
        cost += op->calculateTalkingCost(minute, age);
    }
    if (bill->check(cost)) {
        bill->add(cost);
        cout << name << " поговорив з " << other.getName() << " " << minute << " хв. Вартість: " << cost << "\n";
    } else {
        cout << "Ліміт рахунку перевищено!\n";
    }
}

void Customer::message(Customer& other, int quantity) {
    if (!bill) { cout << name << " не має рахунку.\n"; return; }
    if (operators.empty()) { cout << name << " не має оператора.\n"; return; }
    double cost = 0;
    for (Operator* op : operators) {
        for (Operator* op_other : other.operators) {
            cost += op->calculateMessageCost(quantity, op->getID(), op_other->getID());
        }
    }
    if (bill->check(cost)) {
        bill->add(cost);
        cout << name << " відправив " << quantity << " повідомлень до " << other.getName() << ". Вартість: " << cost << "\n";
    } else {
        cout << "Ліміт рахунку перевищено!\n";
    }
}

void Customer::connection(double amount) {
    if (!bill) { cout << name << " не має рахунку.\n"; return; }
    if (operators.empty()) { cout << name << " не має оператора.\n"; return; }
    double cost = 0;
    for (Operator* op : operators) {
        cost += op->calculateNetworkCost(amount);
    }
    if (bill->check(cost)) {
        bill->add(cost);
        cout << name << " використав інтернет: " << amount << " MB. Вартість: " << cost << "\n";
    } else {
        cout << "Ліміт рахунку перевищено!\n";
    }
}

void Customer::payBill(double amount) {
    if (!bill) { cout << name << " не має рахунку.\n"; return; }
    bill->pay(amount);
    cout << name << " сплатив " << amount << ". Поточний борг: " << bill->getCurrentDebt() << "\n";
}

void Customer::changeOperator(Operator* newOp) {
    if (!newOp) return;
    for (Operator* op : operators) {
        op->removeCustomer(this);
    }
    operators.clear();
    addOperator(newOp);
    cout << name << " змінив оператора на ID " << newOp->getID() << "\n";
}

void Customer::changeBillLimit(double newLimit) {
    if (!bill) { cout << name << " не має рахунку.\n"; return; }
    bill->changeTheLimit(newLimit);
    cout << name << " змінив ліміт рахунку на " << newLimit << "\n";
}

void Customer::showInfo() {
    cout << "ID: " << ID << " | " << name << " | Вік: " << age
         << " | Борг: " << bill->getCurrentDebt() << " / " << bill->getLimitingAmount() << " | Оператори: ";
    for (Operator* op : operators) cout << op->getID() << " ";
    cout << "\n";
}


int main() {
    Operator op1(0, 0.5, 0.2, 0.1, 20);
    Operator op2(1, 0.6, 0.25, 0.12, 15);
    Operator op3(2, 0.4, 0.18, 0.09, 10);

    Bill bill1(100);
    Bill bill2(80);

    Customer c1(0, "Остап", 17, &op1, &bill1);
    Customer c2(1, "Марія", 30, &op2, &bill2);

    c1.addOperator(&op2);
    c2.addOperator(&op1);

    cout << "\n--- Початкова інформація ---\n";
    c1.showInfo();
    c2.showInfo();

    cout << "\n--- Перевірка дій ---\n";
    c1.talk(c2, 10);
    c2.message(c1, 5);
    c1.connection(50);

    c1.payBill(20);
    c2.changeBillLimit(200);
    c1.changeOperator(&op3);

    cout << "\n--- Фінальний стан ---\n";
    c1.showInfo();
    c2.showInfo();

    cout << "\n--- Клієнти кожного оператора ---\n";
    op1.showCustomers();
    op2.showCustomers();
    op3.showCustomers();

    return 0;
}
