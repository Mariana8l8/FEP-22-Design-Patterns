using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class Practice : Session
    {
        public Practice(TimeCell time, string room, ITeacher teacher) : base(time, room, teacher) { }
        protected override void EnsureRole(ITeacher teacher)
        {
            if (teacher is not IPracticalCapable) throw new ArgumentException("Teacher must be lecture-capable.");
        }
    }
}
