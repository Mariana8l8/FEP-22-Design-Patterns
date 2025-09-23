using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab2_patterns
{
    internal interface IHub
    {
        public int ID { get; }
        public double Latitude { get; } 
        public double Longitude { get; }
        public double DistanceTo(IHub other);
    }
}
