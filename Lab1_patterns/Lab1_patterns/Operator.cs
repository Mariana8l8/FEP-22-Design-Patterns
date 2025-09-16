using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab1_patterns
{

    /// <summary>
    /// Provides pricing and discount rules for telecom services (voice, messages, data)
    /// and manages customer billing.
    /// </summary>
    internal class Operator
    {

        /// <summary>
        /// Unique identifier of this operator instance.
        /// Assigned automatically from <see cref="nextId"/>.
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Global counter used to assign unique <see cref="Id"/> values to operators.
        /// </summary>
        private static int nextId;

        /// <summary>
        /// Base price per 1 minute of voice call for this operator (before discounts).
        /// </summary>
        public double TalkingCharge { get; }

        /// <summary>
        /// Base price per 1 message (SMS/IM) for this operator (before discounts).
        /// </summary>
        public double MessageCost { get; }

        /// <summary>
        /// Base price per 1 MB of mobile data for this operator (before discounts).
        /// </summary>
        public double NetworkCharge { get; }

        /// <summary>
        /// Discount percentage (0–100) applied when eligibility conditions are met.
        /// </summary>
        public double DiscountRate { get; set; }

        /// <summary>
        /// Determines whether the given age qualifies for an age-based discount.
        /// True for &lt; 18 or &gt; 65.
        /// </summary>
        /// <param name="age">Customer age.</param>
        private static bool AgeDiscount(int age) => age < 18 || age > 65;

        /// <summary>
        /// Global store of bills by customer ID, shared across all <see cref="Operator"/> instances.
        /// </summary>
        public static Dictionary<int, Bill> bills { get; set; } = new Dictionary<int, Bill>();

        /// <summary>
        /// Initializes a new operator instance with voice, message, and data rates, and a base discount.
        /// </summary>
        /// <param name="talkingCharge">Price per 1 minute of voice call.</param>
        /// <param name="messageCost">Price per 1 message (SMS/IM).</param>
        /// <param name="networkCharge">Price per 1 MB of mobile data.</param>
        /// <param name="discountRate">Discount percentage (0–100).</param>
        public Operator(double talkingCharge, double messageCost, double networkCharge, double discountRate)
        {
            this.Id = nextId++;
            this.TalkingCharge = talkingCharge;
            this.MessageCost = messageCost;
            this.NetworkCharge = networkCharge;
            this.DiscountRate = discountRate;
            Console.WriteLine("\nCreated operator!\n");
        }

        /// <summary>
        /// Calculates the cost of a voice call, applying a discount when eligible.
        /// A discount applies if both customers use the same operator or the caller qualifies
        /// for an age-based discount (under 18 or over 65) and <see cref="DiscountRate"/>
        /// </summary>
        /// <param name="min">Call duration in minutes.</param>
        /// <param name="customer">Caller.</param>
        /// <param name="other">Receiver.</param>
        /// <returns>Total call cost.</returns>
        public double CalculateTalkingCost(int min, Customer customer, Customer other)
        {
            double cost = min * TalkingCharge;
            if (customer.ActiveOperator == other.ActiveOperator && DiscountRate > 0 || AgeDiscount(customer.Age) && DiscountRate > 0)
            {
                cost *= (100 - DiscountRate) / 100.0;
                Console.WriteLine("Discount activated!\n");
            }
            Console.WriteLine($"Talking cost: {cost}\n");
            return cost;
        }

        /// <summary>
        /// Calculates the cost of sending messages.
        /// A discount applies only if both customers use the same operator
        /// and <see cref="DiscountRate"/> &gt; 0.
        /// </summary>
        /// <param name="quantity">Number of messages.</param>
        /// <param name="customer">Sender.</param>
        /// <param name="other">Receiver.</param>
        /// <returns>Total message cost.</returns>
        public double CalculateMessageCost(int quantity, Customer customer, Customer other)
        {
            double cost = quantity * MessageCost;
            if (customer.ActiveOperator == other.ActiveOperator && DiscountRate > 0)
            {
                cost *= (100 - DiscountRate) / 100.0;
                Console.WriteLine("Discount activated!\n");
            }
            Console.WriteLine($"Message cost: {cost}\n");
            return cost;
        }

        /// <summary>
        /// Calculates the cost of mobile data usage without discounts.
        /// </summary>
        /// <param name="amountMB">Data volume in megabytes.</param>
        /// <param name="customer">Customer for whom the cost is calculated.</param>
        /// <returns>Data cost: <c>amountMB * NetworkCharge</c>.</returns>
        public double CalculateNetworkCost(double amountMB, Customer customer)
        {
            double cost = amountMB * NetworkCharge;
            Console.WriteLine($"Network cost: {cost}\n");
            return cost;
        }

        /// <summary>
        /// Connects this operator to the specified customer and creates a bill if it does not already exist.
        /// </summary>
        /// <param name="customer">Customer to connect.</param>
        /// <param name="amountLimit">Spending limit for the new bill.</param>
        public void ConnectionToTheOperator(Customer customer, double amountLimit = 0)
        {
            bool firstConnecting = true;
            if (customer.operators.ContainsKey(Id) ) Console.WriteLine("Operator already connected!\n");
            else
            {
                customer.operators.Add(Id, this);
                Console.WriteLine($"The operator has been successfully connected to the {customer.Name}.\n");
                if (firstConnecting)
                {
                    CreateBill(customer.Id, amountLimit);
                    firstConnecting = false;
                }
            }
        }

        /// <summary>
        /// Creates a bill for the customer with the specified ID, or returns the existing one.
        /// Bills are stored in the static <see cref="bills"/> dictionary (key = customer ID).
        /// </summary>
        /// <param name="id">Customer ID.</param>
        /// <param name="amountLimit">Spending limit to set for the bill.</param>
        /// <returns>The <see cref="Bill"/> instance (new or existing).</returns>
        public Bill CreateBill(int id, double amountLimit) 
        {
            if (bills.ContainsKey(id))
            {
                Console.WriteLine("Bill already exists!");
                return bills[id];
            }
            else
            {
                var bill = new Bill(amountLimit);
                bills.Add(id, bill);
                Console.WriteLine("Bill successfully created!");
                return bill;
            }
        } 
    }
}
