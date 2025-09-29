using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab3_patterns.Tests
{
    public class CourseAbstractFactoryTests
    {
        [Fact]
        public void ProgrammingCourseFactory_CreateLecture_ReturnsProgrammingLecture()
        {
            ICourseFactory factory = new ProgrammingCourseFactory();

            var lecturer = new Lecturer("Oleh Sinkevych");
            var lecture = factory.CreateLecture(new TimeCell(DayOfWeek.Wednesday, new TimeOnly(15, 05), new TimeOnly(16, 25)), "129/T", lecturer);

            Assert.IsType<ProgrammingLecture>(lecture);
        }

        [Fact]
        public void DatabasesCourseFactory_CreateCourseWork_ReturnsDatabasesCourseWork()
        {
            ICourseFactory factory = new DatabasesCourseFactory();

            var mentor = new ExternalMentor("Oleh Sinkevych");
            var coursework = factory.CreateCoursework(mentor);

            Assert.IsType<DatabasesCoursework>(coursework);
        }
    } 
}
