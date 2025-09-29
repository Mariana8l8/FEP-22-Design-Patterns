using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class StudentGroup
    {
        public string Name { get; }
        public List<Session> Schedule { get; set; } = new();
        public List<CourseEnrollment> Courses { get; set; } = new();
        public List<Coursework> CourseWorks { get; } = new();


        public StudentGroup(string name) => Name = string.IsNullOrWhiteSpace(name) ? throw new ArgumentException("Name required") : name;


        public void AddSession(Session session)
        {
            session = session ?? throw new ArgumentNullException(nameof(session));
            if (!CheckConflicts(session)) { Schedule.Add(session); }
        }
        public void RemoveSession(Session session)
        {
            session = session ?? throw new ArgumentNullException(nameof(session));
            Schedule.Remove(session);
        }
        public bool CheckConflicts(Session session)
        {
            session = session ?? throw new ArgumentNullException(nameof(session));
            foreach (var s in Schedule)
            {
                if (session.Time.CheckOverlay(s.Time))
                {
                    throw new InvalidOperationException("Session time conflicts with existing schedule.");
                }
            }
            return false;
        }

        public CourseEnrollment Enroll(
        ICourseFactory factory,
        Lecturer lecturer,
        Assistant assistant,
        ISuperviseCapable supervisor,
        TimeCell lectureTime,
        TimeCell practicalTime,
        string lectureRoom,
        string practicalRoom)
        {
            if (factory == null) throw new ArgumentNullException(nameof(factory));
            if (lecturer == null) throw new ArgumentNullException(nameof(lecturer));
            if (assistant == null) throw new ArgumentNullException(nameof(assistant));
            if (supervisor == null) throw new ArgumentNullException(nameof(supervisor));
            if (lectureTime == null) throw new ArgumentNullException(nameof(lectureTime), "Lecture time is required");
            if (practicalTime == null) throw new ArgumentNullException(nameof(practicalTime), "Practical time is required");
            if (lectureRoom == null) throw new ArgumentNullException(nameof(lectureRoom), "Lecture room is required");
            if (practicalRoom == null) throw new ArgumentNullException(nameof(practicalRoom), "Practical room is required");

            var lecture = factory.CreateLecture(lectureTime, lectureRoom, lecturer);
            var practice = factory.CreatePractical(practicalTime, practicalRoom, assistant);
            var coursework = factory.CreateCoursework(supervisor);

            AddSession(lecture);
            AddSession(practice);
            CourseWorks.Add(coursework);

            var enrollment = new CourseEnrollment(factory.CourseName, lecture, practice, coursework, lectureRoom, practicalRoom);
            Courses.Add(enrollment);
            return enrollment;
        }
    }
}
