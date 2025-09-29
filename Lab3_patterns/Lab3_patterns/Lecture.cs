using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class Lecture : Session
    {
        public Lecture(TimeCell time, string room, ITeacher teacher) : base(time, room, teacher) { }
        protected override void EnsureRole(ITeacher teacher)
        {
            if (teacher is not ILectureCapable) throw new ArgumentException("Teacher must be lecture-capable.");
        }
    }
}
