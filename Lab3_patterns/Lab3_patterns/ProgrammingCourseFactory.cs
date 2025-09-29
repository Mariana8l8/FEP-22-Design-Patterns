using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class ProgrammingCourseFactory : ICourseFactory
    {
        public string CourseName => "Programming";
        public Session CreateLecture(TimeCell time, string room, Lecturer lecturer) => new ProgrammingLecture(time, room, lecturer);
        public Session CreatePractical(TimeCell time, string room, Assistant assistant) => new ProgrammingPractice(time, room, assistant);
        public Coursework CreateCoursework(ISuperviseCapable supervisor) => new ProgrammingCoursework("Programming Coursework", new GitHubRepoDefense(), supervisor);
    }
}
