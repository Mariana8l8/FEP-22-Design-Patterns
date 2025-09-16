namespace Lab01;

internal class Operator
{
    private static int _nextId;
    public int Id { get; }
    public double TalkingCharge { get; }
    public double MessageCost { get; }
    public double NetworkCharge { get; }
    public double DiscountRate { get; set; }
    public Dictionary<int, Bill> Bills { get; } = new();

    public Operator(double talkingCharge, double messageCost, double networkCharge, double discountRate)
    {
        Id = _nextId++;
        TalkingCharge = talkingCharge;
        MessageCost = messageCost;
        NetworkCharge = networkCharge;
        DiscountRate = discountRate;
    }

    private double CalculateTalkingCost(int minutes, Customer customer)
    {
        double discount = customer.Age is <= 18 or > 65 ? DiscountRate : 0;
        return TalkingCharge * minutes * (1 - discount);
    }

    private double CalculateMessageCost(int quantity, Customer customer1, Customer customer2)
    {
        double discount = customer1.Operators.ContainsKey(Id) && customer2.Operators.ContainsKey(Id) ? DiscountRate : 0;
        return quantity * MessageCost * (1 - discount);
    }

    private double CalculateNetworkCost(double amount)
    {
        return NetworkCharge * amount;
    }

    public void SignCustomer(Customer customer)
    {
        Bills.Add(customer.Id, new Bill(100));
    }

    public void UnsignCustomer(Customer customer)
    {
        Bills.Remove(customer.Id);
    }

    public void ChangeLimit(double limit, int clientId)
    {
        Bills[clientId].ChangeLimit(limit);
    }

    public void HandleCall(Customer c1, Customer c2, int minutes)
    {
        double price = CalculateTalkingCost(minutes, c1);

        if (Bills[c1.Id].Check(price))
        {
            Console.WriteLine($"Customer {c1.Id} is successfully connected to customer {c2.Id} by phone.");
            Bills[c1.Id].AddDebt(price);
        }
        else
        {
            Console.WriteLine("Limit exceeded! Pay your debt first.");
        }
    }

    public void HandleMessage(Customer c1, Customer c2, int quantity)
    {
        double price = CalculateMessageCost(quantity, c1, c2);

        if (Bills[c1.Id].Check(price))
        {
            Console.WriteLine($"Customer {c1.Id} has successfully sent {quantity} messages to customer {c2.Id}.");
            Bills[c1.Id].AddDebt(price);
        }
        else
        {
            Console.WriteLine("Limit exceeded! Pay your debt first.");
        }
    }

    public void HandleNetworkConnection(Customer c1, int quantity)
    {
        double price = CalculateNetworkCost(quantity);

        if (Bills[c1.Id].Check(price))
        {
            Console.WriteLine($"Customer {c1.Id} was successfully connected to the network.");
            Bills[c1.Id].AddDebt(price);
        }
        else
        {
            Console.WriteLine("Limit exceeded! Pay your debt first.");
        }
    }
}