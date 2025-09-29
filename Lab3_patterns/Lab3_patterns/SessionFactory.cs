using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public abstract class SessionFactory
    {
        public Session CreateSession(TimeCell time, string room, ITeacher teacher) => Make(time, room, teacher);
        public abstract Session Make(TimeCell time, string room, ITeacher teacher);
    }
}
