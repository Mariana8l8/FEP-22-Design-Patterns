namespace Lab01;

internal class Customer
{
    private static int _nextId;
    public int Id { get; }
    public string Name { get; }
    public int Age { get; set; }
    public Dictionary<int, Operator> Operators { get; } = new();

    public Customer(string name, int age)
    {
        Id = _nextId++;
        Name = name;
        Age = age;
    }

    public void ChangeLimit(double limit, int operatorId)
    {
        Operators[operatorId].ChangeLimit(limit, Id);
    }
    public void MakeCall(int minutes, Customer customer, Operator op)
    {
        op.HandleCall(this, customer, minutes);
    }

    public void SendMessage(int number, Customer customer, Operator op)
    {
        op.HandleMessage(this, customer, number);
    }

    public void ConnectToInternet(int quantity, Operator op)
    {
        op.HandleNetworkConnection(this, quantity);
    }
       
    public void Sign(Operator op)
    {
        if (Operators.TryAdd(op.Id, op))
        {
            Console.WriteLine($"Customer {Id} has successfully signed to operator {op.Id}.");
            op.SignCustomer(this);
        }
        else
        {
            Console.WriteLine($"Customer {Id} is already signed to operator {op.Id}.");
        }
    }

    public void Unsign(Operator op)
    {
        if (Operators.Remove(op.Id))
        {
            Console.WriteLine($"Customer {Id} has unsigned from operator {op.Id}.");
            op.UnsignCustomer(this);
        }
        else
        {
            Console.WriteLine($"Customer {Id} wasn't signed to operator {op.Id}.");
        }
    }
}