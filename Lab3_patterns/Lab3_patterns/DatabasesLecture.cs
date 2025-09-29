using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class DatabasesLecture : Lecture
    {
        public DatabasesLecture(TimeCell time, string room, ITeacher teacher) : base(time, room, teacher) { }
    }
}
