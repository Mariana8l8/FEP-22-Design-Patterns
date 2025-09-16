using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Lab1_patterns
{

    /// <summary>
    /// Represents a telecom customer with identity, age, an active operator, and
    /// a set of subscribed operators. Provides actions to call, message, and use data.
    /// </summary>
    internal class Customer
    {
        /// <summary>
        /// Global counter used to assign unique <see cref="Id"/> values to customers.
        /// </summary>
        private static int customerId;

        /// <summary>
        /// Unique identifier of this customer, assigned automatically.
        /// </summary>
        public int Id { get; }

        /// <summary>
        /// Customer's display name.
        /// </summary>
        public string Name { get; }

        /// <summary>
        /// Customer's age (used for potential age-based discounts).
        /// </summary>
        public int Age { get; }

        /// <summary>
        /// The currently active <see cref="Operator"/> used to calculate costs.
        /// Can be <c>null</c> until set.
        /// </summary>
        public Operator? ActiveOperator { get; set; }

        /// <summary>
        /// Subscribed operators keyed by operator ID.
        /// Key: operator ID; Value: <see cref="Operator"/> instance.
        /// </summary>
        public Dictionary<int, Operator> operators { get; set; } = new Dictionary<int, Operator>();

        /// <summary>
        /// Creates a new customer with name and age. The active operator is not set.
        /// </summary>
        /// <param name="name">Customer name.</param>
        /// <param name="age">Customer age.</param>
        public Customer(string name, int age)
        {
            Console.WriteLine("\nCreated customer!\n");
            this.Id = customerId++;
            this.Name = name;
            this.Age = age;
            this.ActiveOperator = null;
        }
        /// <summary>
        /// Sets the active operator by its ID from the <see cref="operators"/> dictionary
        /// if the active operator is not already set.
        /// </summary>
        /// <param name="operatorId">The ID of the operator to set active.</param>
        public void SetActiveOperatorById(int operatorId)
        {
            if (!operators.ContainsKey(operatorId))
            {
                Console.WriteLine("Please, connect to the operator!");
            }
            else
            {
                if (ActiveOperator == null)
                {
                    ActiveOperator = operators[operatorId];
                    Console.WriteLine("The active operator was successfully seted\n");
                }
                else
                {
                    Console.WriteLine($"The active operator is already set \"{ActiveOperator}\". Change it if necessary.");
                }
            }
        }
        /// <summary>
        /// Switches the active operator to the specified instance.
        /// </summary>
        /// <param name="op">Operator instance to make active.</param>
        public void ChangeActiveOperator(Operator op) { ActiveOperator = op; Console.WriteLine("Operator successfully changed!\n"); }

        /// <summary>
        /// Switches the active operator to the operator with the given ID.
        /// </summary>
        /// <param name="operatorId">The ID of the operator to activate.</param>
        /// <returns><c>true</c> if the operator was changed; otherwise, <c>false</c>.</returns>
        public bool ChangeActiveOperatorById(int operatorId)
        {
            var op = operators[operatorId];
            if (op != null)
            {
                ActiveOperator = op;
                Console.WriteLine("The operator was successfully changed!\n");
                return true;
            }
            else { Console.WriteLine("The operator was not changed!\n"); return false; }
        }

        /// <summary>
        /// Makes a voice call to another customer using the current <see cref="ActiveOperator"/>.
        /// Charges the call cost to the customer's bill if within the limit.
        /// </summary>
        /// <param name="min">Call duration in minutes.</param>
        /// <param name="other">The receiving customer.</param>
        public void Talk(int min, Customer other)
        {
            if (ActiveOperator == null) { Console.WriteLine("To start, set the active operator!\n"); }
            else
            {
                double cost = ActiveOperator.CalculateTalkingCost(min, this, other);
                if (Operator.bills[Id].TryCharge(cost)) Console.WriteLine("The call is successful!\n");
                else Console.WriteLine("The call is unsuccessful!\n");
            }
        }

        /// <summary>
        /// Sends messages to another customer using the current <see cref="ActiveOperator"/>.
        /// Charges the total message cost to the customer's bill if within the limit.
        /// </summary>
        /// <param name="quantity">Number of messages to send.</param>
        /// <param name="other">The receiving customer.</param>
        public void Message(int quantity, Customer other)
        {
            if (ActiveOperator == null) { Console.WriteLine("To start, set the active operator!\n"); }
            else
            {
                double cost = ActiveOperator.CalculateMessageCost(quantity, this, other);
                if (Operator.bills[Id].TryCharge(cost)) Console.WriteLine("The message was sent successfully!\n");
                else Console.WriteLine("The message was not sent!\n");
            }
        }

        /// <summary>
        /// Uses mobile data via the current <see cref="ActiveOperator"/> and charges the cost to the bill.
        /// </summary>
        /// <param name="amount">Amount of data to consume (in MB).</param>
        public void Connection(double amount)
        {
            if (ActiveOperator == null) { Console.WriteLine("To start, set the active operator!\n"); }
            else
            {
                double cost = ActiveOperator.CalculateNetworkCost(amount, this);
                if (Operator.bills[Id].TryCharge(cost)) Console.WriteLine("The connection is successful!\n");
                else Console.WriteLine("The connection is unsuccessful!\n");
            }
        }
    }
}
