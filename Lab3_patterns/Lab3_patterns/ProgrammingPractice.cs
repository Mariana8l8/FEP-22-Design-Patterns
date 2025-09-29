using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class ProgrammingPractice : Practice
    {
        public ProgrammingPractice(TimeCell time, string room, ITeacher teacher) : base(time, room, teacher) { }
    }
}
