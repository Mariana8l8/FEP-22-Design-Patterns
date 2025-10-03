from datetime import date

from courses.programming_course import ProgrammingCourse
from factories.lecture_factory import LectureFactory
from factories.practice_factory import PracticeFactory
from group.student_group import StudentGroup
from roles.assistant import Assistant
from roles.lecturer import Lecturer

lecturer = Lecturer(name="Dr. Smith")
assistant = Assistant(name="Mr. Johnson")

lecture_data = (
    (1, 101, date(2025, 10, 3)),
    (2, 101, date(2025, 10, 5)),
    (3, 101, date(2025, 10, 7)),
)

practice_data = (
    (1, 201, date(2025, 10, 3)),
    (2, 201, date(2025, 10, 5)),
)

lecture_factory = LectureFactory()
lectures = lecture_factory.create(lecture_data, lecturer)

practice_factory = PracticeFactory()
practices = practice_factory.create(practice_data, assistant)

course = ProgrammingCourse(
    name="Programming 101",
    lecturer=lecturer,
    assistant=assistant,
    future_lectures=lectures.copy(),
    future_practices=practices.copy()
)

group = StudentGroup("FEP-22")
group.enroll(course)

print("\n--- Lectures ---")
for lecture in lectures:
    group.attend_session("Programming 101", lecture)
    group.leave_session("Programming 101")


print("\n--- Course Progress ---")
group.show_course_progress("Programming 101")

print("\n--- Practices ---")
for practice in practices:
    group.attend_session("Programming 101", practice)
    group.leave_session("Programming 101")

print("\n--- Course Progress ---")
group.show_course_progress("Programming 101")