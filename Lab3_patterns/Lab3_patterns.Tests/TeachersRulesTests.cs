using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns.Tests
{
    public class TeachersRulesTests
    {
        [Fact]
        public void Lecturer_CanBeAssignedToLecture()
        {
            var lecturer = new Lecturer("Oleh Sinkevych");
            var lecture = new Lecture(new TimeCell(DayOfWeek.Wednesday, new TimeOnly(15, 05), new TimeOnly(16, 25)), "129/T", lecturer);

            Assert.Same(lecture.Teacher, lecturer);
        }

        [Fact]
        public void ExternalMentor_CannotBeAssignedToLecture_Throws()
        {
            var mentor = new ExternalMentor("Oleh Sinkevych");

            Assert.Throws<ArgumentException>(() => new Lecture(new TimeCell(DayOfWeek.Monday, new TimeOnly(15, 05), new TimeOnly(16, 25)), "129/T", mentor));
        }
    }
}
