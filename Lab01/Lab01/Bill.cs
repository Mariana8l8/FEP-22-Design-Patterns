namespace Lab01;

internal class Bill
{
    public double Limit { get; set; }
    public double Debt { get; set; }

    public Bill(int limit)
    {
        Limit = limit;
        Debt = 0;
    }

    public bool Check(double amount)
    {
        return Debt + amount < Limit;
    }

    public void ChangeLimit(double amount)
    {
        Console.WriteLine($"Limit was changed from {Limit}$ to {amount}$.");
        Limit = amount;
    }

    public void AddDebt(double amount)
    {
        Debt += amount;
        Console.WriteLine($"{amount}$ added to debt. Current debt: {Debt}.");
    }

    public void Pay(double amount)
    {
        Debt -= amount;
        Console.WriteLine($"{amount}$ subtracted from debt. Current debt: {Debt}.");
    }
}