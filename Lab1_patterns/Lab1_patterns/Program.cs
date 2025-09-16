
using Lab1_patterns;

class Program
{
    static void Main(string[] args)
    {
        Operator lifecell = new Operator(2, 0.5, 0.05, 10);
        Operator kyivStar = new Operator(3, 0.6, 0.06, 15);
        Operator VodaFone = new Operator(4, 0.7, 0.07, 16);

        Customer customer1 = new Customer("Mariana", 17);
        Customer customer2 = new Customer("Anastasiia", 18);

        lifecell.ConnectionToTheOperator(customer1, 20);
        VodaFone.ConnectionToTheOperator(customer2, 100);

        customer1.SetActiveOperatorById(0);
        customer2.SetActiveOperatorById(0);

        customer1.Talk(10, customer2);
        customer1.Message(5, customer2);
        customer1.Connection(100);

        VodaFone.ConnectionToTheOperator(customer1);
        customer1.Talk(10, customer2 );
    }
}