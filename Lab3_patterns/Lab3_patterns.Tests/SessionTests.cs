namespace Lab3_patterns.Tests
{
    public class SessionTests
    {
        [Fact]
        public void LectureFactory_CreateSession_ReturnsLectureSession()
        {
            var factory = new LectureFactory();
            var teacher = new Lecturer("Oleh Sinkevych");

            var session = factory.CreateSession(new TimeCell(DayOfWeek.Wednesday, new TimeOnly(15, 05), new TimeOnly(16, 25)), "129/T", teacher);

            Assert.IsType<Lecture>(session);
        }

        [Fact]
        public void PracticalFactory_CreateSession_ReturnsPracticalSession()
        {
            var factory = new PracticeFactory();
            var teacher = new Assistant("Oleh Sinkevych");

            var session = factory.CreateSession(new TimeCell(DayOfWeek.Tuesday, new TimeOnly(16, 40), new TimeOnly(18, 00)), "4/T", teacher);

            Assert.IsType<Practice>(session);
        }
    }
}
