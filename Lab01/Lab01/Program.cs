namespace Lab01;

internal class Program
{
    static void Main()
    {
        Customer c1 = new Customer("John", 16);
        Customer c2 = new Customer("Alice", 32);

        Operator o1 = new Operator(10, 5, 7, 0.3);
        Operator o2 = new Operator(15, 3, 5, 0.1);

        c1.Sign(o1);
        c1.Sign(o2);

        c2.Sign(o1);

        c1.MakeCall(3, c2, o1);
        c1.SendMessage(2, c2, o1);
        c1.ConnectToInternet(5, o1);
    }
}