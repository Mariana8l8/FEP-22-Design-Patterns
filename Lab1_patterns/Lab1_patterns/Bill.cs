using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;

namespace Lab1_patterns
{
    /// <summary>
    /// Represents a customer's bill with a spending limit and current outstanding debt.
    /// Provides operations to check/charge amounts, make payments, and change the limit.
    /// </summary>
    internal class Bill
    {
        /// <summary>
        /// The maximum allowed debt. New charges are rejected if they would exceed this value.
        /// </summary>
        public double LimitingAmount {  get; private set; }

        /// <summary>
        /// The current outstanding debt (never less than zero).
        /// </summary>
        public double CurrentDebt { get; private set; }

        /// <summary>
        /// Creates a new bill with the specified spending limit and zero initial debt.
        /// </summary>
        /// <param name="limit">The debt limit for this bill.</param>
        public Bill(double limit)
        {
            this.LimitingAmount = limit;
            this.CurrentDebt = 0;
            Console.WriteLine("\nCreated bill!\n");
        }

        /// <summary>
        /// Checks whether a charge of the given amount fits within the spending limit.
        /// </summary>
        /// <param name="amount">The amount to test (assumed non-negative).</param>
        public bool Check(double amount) => CurrentDebt + amount <= LimitingAmount;


        /// <summary>
        /// Adds the specified amount to the current debt (no limit check here).
        /// </summary>
        /// <param name="amount">The amount to add to the debt (assumed non-negative).</param>
        public void Add(double amount)
        {
            CurrentDebt += amount;
            Console.WriteLine($"Current debt after adding: {CurrentDebt}\n");
        }

        /// <summary>
        /// Pays down the current debt by the specified amount. If the payment exceeds the debt,
        /// the debt is set to zero and the overpay amount is printed to the console.
        /// </summary>
        /// <param name="amount">The payment amount (assumed non-negative).</param>
        public void Pay(double amount)
        {
            double newDebt = CurrentDebt - amount;
            double overpay = newDebt < 0 ? -newDebt : 0;
            CurrentDebt = newDebt > 0 ? newDebt : 0;

            Console.WriteLine($"Overpay: {overpay}\n");
            Console.WriteLine($"Current debt: {CurrentDebt}\n");
        }

        /// <summary>
        /// Sets a new spending limit for this bill.
        /// </summary>
        /// <param name="amount">The new limit value.</param>
        public void ChangeTheLimit(double amount)
        {
            LimitingAmount = amount;
            Console.WriteLine($"Current limit: {LimitingAmount}\n");
        }

        /// <summary>
        /// Attempts to charge the specified amount, enforcing the spending limit.
        /// </summary>
        /// <param name="amount">The amount to charge (assumed non-negative).</param>
        public bool TryCharge(double amount)
        {
            if (!Check(amount))
            {
                Console.WriteLine("Limiting amount exceeded!\n");
                return false;
            }
            Console.WriteLine("Limiting amount NOT exceeded!\n");
            Add(amount); 
            return true;
        }
    }
}
