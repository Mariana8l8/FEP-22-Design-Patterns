﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
namespace Lab2_patterns
{
    internal interface IShip : ITransport<IPort>
    {
        List<Container> CurrentContainers { get; }
        public void ReFuel(double newFuel);
        public bool Load(Container cont);
        public bool Unload(Container cont);
        public double WeightTotalCalc(List<Container> currentContainers);
    }
}
