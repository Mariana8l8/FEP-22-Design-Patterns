using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class PracticeFactory : SessionFactory
    {
        public override Session Make(TimeCell time, string room, ITeacher teacher) => new Practice(time, room, teacher);
    }
}
