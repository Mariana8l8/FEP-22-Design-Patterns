using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public interface ICourseFactory
    {
        public string CourseName { get; }
        Session CreateLecture(TimeCell time, string room, Lecturer lecturer);
        Session CreatePractical(TimeCell time, string room, Assistant assistant);
        Coursework CreateCoursework(ISuperviseCapable supervisor);
    }
}
