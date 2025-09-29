using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class ProgrammingLecture : Lecture
    {
        public ProgrammingLecture(TimeCell time, string room, ITeacher teacher) : base(time, room, teacher) { }
    }
}
