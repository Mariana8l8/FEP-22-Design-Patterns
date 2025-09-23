using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab2_patterns
{
    internal interface IPort : IHub
    {
        public List<IShip> Current { get; }
        public List<Container> Containers { get; }
        public void IncomingShip(IShip s);
        public void OutgoingShip(IShip s);
    }
}

