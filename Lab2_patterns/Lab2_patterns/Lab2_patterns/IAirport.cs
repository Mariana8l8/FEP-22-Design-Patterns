using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab2_patterns
{
    internal interface IAirport : IHub
    {
        public int MaxGates { get; }
        public void IncomingPlane(IPlane plane);
        public void OutgoingPlane(IPlane plane);
        public List<IPlane> Current { get; }
    }
}
