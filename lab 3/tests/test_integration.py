import pytest
from scheduling.courses import ProgrammingCourseFactory
from scheduling.teachers import Lecturer, Assistant, ExternalMentor
from scheduling.groups import StudentGroup

def test_group_enrollment_and_conflict_detection():
    course_factory = ProgrammingCourseFactory()
    lecturer = Lecturer("Dr. Oleh Sinkevych")
    assistant = Assistant("Dr. Mariia Petrenko")
    mentor = ExternalMentor("Industry Expert")

    group = StudentGroup("FeP-22")
    coursework = group.enroll(course_factory, lecturer, assistant, mentor)

    conflicts = group.check_conflicts()
    assert len(conflicts) == 0  # у демо немає конфліктів
    assert coursework.supervisor == mentor
