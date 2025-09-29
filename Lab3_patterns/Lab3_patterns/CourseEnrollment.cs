using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns
{
    public class CourseEnrollment
    {
        public string CourseName { get; }
        public Session Lecture { get; }
        public Session Practical { get; }
        public Coursework Coursework { get; }
        public string LectureRoom {  get; }
        public string PracticalRoom {  get; }


        public CourseEnrollment(string courseName, Session lecture, Session practical, Coursework coursework, string lectureRoom, string practicalRoom)
        {
            this.CourseName = string.IsNullOrWhiteSpace(courseName) ? throw new ArgumentException("Course name required") : courseName;
            this.Lecture = lecture ?? throw new ArgumentNullException(nameof(lecture));
            this.Practical = practical ?? throw new ArgumentNullException(nameof(practical));
            this.Coursework = coursework ?? throw new ArgumentNullException(nameof(coursework));
            this.LectureRoom = string.IsNullOrWhiteSpace(lectureRoom) ? throw new ArgumentNullException(nameof(lectureRoom)) : lectureRoom;
            this.PracticalRoom = string.IsNullOrWhiteSpace(practicalRoom) ? throw new ArgumentNullException(nameof(practicalRoom)) : practicalRoom;
        }
    }
}
