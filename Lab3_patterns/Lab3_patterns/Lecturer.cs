using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class Lecturer : ITeacher, ILectureCapable, ISuperviseCapable
    {
        public string Name { get; }
        public Lecturer(string name) => this.Name = string.IsNullOrWhiteSpace(name) ? throw new ArgumentException("Name required") : name;
    }
}
