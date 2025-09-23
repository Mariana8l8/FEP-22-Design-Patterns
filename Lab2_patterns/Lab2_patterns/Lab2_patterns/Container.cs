using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab2_patterns
{
    internal abstract class Container
    {
        public int ID { get; }
        public double Weight { get; }

        protected Container(int id, double weight)
        {
            ID = id;
            Weight = weight;
        }

        public abstract double Consumption();
        public bool Equals(Container other)
        {
            if (other is null) return false;
            if (this.GetType() == other.GetType() && this.Weight == other.Weight && this.ID == other.ID) return true;
            else return false;
        }
    }
}
