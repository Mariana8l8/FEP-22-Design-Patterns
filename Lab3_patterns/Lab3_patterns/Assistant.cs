using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class Assistant : ITeacher, IPracticalCapable
    {
        public string Name { get; }
        public Assistant(string name) => this.Name = string.IsNullOrWhiteSpace(name) ? throw new ArgumentException("Name required") : name;

    }
}
