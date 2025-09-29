using System;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;


namespace Lab3_patterns
{
    public class CourseConfig
    {
        [JsonPropertyName("course")] public string? Course { get; set; }
        [JsonPropertyName("group")] public string? Group { get; set; }
        [JsonPropertyName("lecturer")] public Person? Lecturer { get; set; }
        [JsonPropertyName("assistant")] public Person? Assistant { get; set; }
        [JsonPropertyName("supervisor")] public Person? Supervisor { get; set; }
        [JsonPropertyName("lecture")] public SessionConfig? Lecture { get; set; }
        [JsonPropertyName("practical")] public SessionConfig? Practical { get; set; }
        [JsonPropertyName("courseworkName")] public string? CourseworkName { get; set; }
    }


    public class Person { public string? Name { get; set; } }


    public class SessionConfig
    {
        public string? Day { get; set; } 
        public string? Start { get; set; } 
        public string? End { get; set; } 
        public string? Room { get; set; } 
    }


    internal class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0 || !File.Exists(args[0]))
            {
                Console.WriteLine("Usage: Lab3_patterns <course.json>");
                return;
            }


            var json = File.ReadAllText(args[0]);
            var config = JsonSerializer.Deserialize<CourseConfig>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });


            if (config is null)
            {
                Console.Error.WriteLine("Invalid JSON.");
                return;
            }


            if (config.Lecture is null || config.Practical is null)
            {
                Console.Error.WriteLine("JSON must contain 'lecture' and 'practical'.");
                return;
            }

            var lecturer = new Lecturer(config.Lecturer?.Name ?? "Lecturer");
            var assistant = new Assistant(config.Assistant?.Name ?? "Assistant");
            var supervisor = new Lecturer(config.Supervisor?.Name ?? "Supervisor"); // any ISuperviseCapable

            var lectureDay = Enum.Parse<DayOfWeek>(config.Lecture.Day ?? "Monday", true);
            var lectureStart = TimeOnly.Parse(config.Lecture.Start ?? "08:30");
            var lectureEnd = TimeOnly.Parse(config.Lecture.End ?? "10:00");
            var lectureTime = new TimeCell(lectureDay, lectureStart, lectureEnd);


            var practicalDay = Enum.Parse<DayOfWeek>(config.Practical.Day ?? "Thursday", true);
            var pracicalStart = TimeOnly.Parse(config.Practical.Start ?? "12:10");
            var practicalEnd = TimeOnly.Parse(config.Practical.End ?? "13:45");
            var practicalTime = new TimeCell(practicalDay, pracicalStart, practicalEnd);


            var lectureRoom = config.Lecture.Room ?? "129";
            var practicalRoom = config.Practical.Room ?? "4";


            var courseName = (config.Course ?? "Programming").Trim();

            Session lecture;
            Session practical;
            Coursework coursework;
            ISubmissionCoursework submission;


            if (string.Equals(courseName, "Programming", StringComparison.OrdinalIgnoreCase))
            {
                lecture = new ProgrammingLecture(lectureTime, lectureRoom, lecturer);
                practical = new ProgrammingPractice(practicalTime, practicalRoom, assistant);
                submission = new GitHubRepoDefense(); 
                coursework = new ProgrammingCoursework(config.CourseworkName ?? "Programming Project", submission, supervisor);
            }
            else if (string.Equals(courseName, "Databases", StringComparison.OrdinalIgnoreCase))
            {
                lecture = new DatabasesLecture(lectureTime, lectureRoom, lecturer);
                practical = new DatabasesPractice(practicalTime, practicalRoom, assistant);
                submission = new OnlineUploadDefense(); 
                coursework = new DatabasesCoursework(config.CourseworkName ?? "Databases Coursework", submission, supervisor);
            }
            else
            {
                lecture = new Lecture(lectureTime, lectureRoom, lecturer);
                practical = new Practice(practicalTime, practicalRoom, assistant);
                submission = new OfflineDefense();
                coursework = new ProgrammingCoursework(config.CourseworkName ?? "Coursework", submission, supervisor);
            }

            var enrollment = new CourseEnrollment(courseName, lecture, practical, coursework, lectureRoom, practicalRoom);


            Console.WriteLine("\nCourse created successfully!\n");
            Console.WriteLine($"Course: {courseName}");
            Console.WriteLine($"Group: {config.Group}");
            Console.WriteLine($"\nLecturer: {config.Lecturer?.Name}");
            Console.WriteLine($"Assistant: {config.Assistant?.Name}");
            Console.WriteLine($"Supervisor: {config.Supervisor?.Name}\n");
            Console.WriteLine($"Lecture: {lectureDay} {lectureStart} - {lectureEnd} № {lectureRoom}");
            Console.WriteLine($"Practical: {practicalDay} {pracicalStart} - {practicalEnd} № {practicalRoom}");
            Console.WriteLine($"\nCoursework: {config.CourseworkName}");  
        }
    }
}