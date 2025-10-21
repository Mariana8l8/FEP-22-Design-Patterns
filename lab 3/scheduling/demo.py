from scheduling.teachers import Lecturer, Assistant, ExternalMentor
from scheduling.courses import ProgrammingCourseFactory
from scheduling.groups import StudentGroup

if __name__ == "__main__":
    lecturer = Lecturer("Dr. Oleh Sinkevych")
    assistant = Assistant("Dr. Mariia Petrenko")
    mentor = ExternalMentor("Industry Expert")

    course_factory = ProgrammingCourseFactory()
    group = StudentGroup("FeP-22")
    coursework = group.enroll(course_factory, lecturer, assistant, mentor)

    print(f"Group: {group.name}")
    for s in group.sessions:
        print(f"{s.__class__.__name__} at {s.time} in {s.room}, teacher: {s.teacher.name}")
    print(f"CourseWork supervised by: {coursework.supervisor.name}")

    conflicts = group.check_conflicts()
    if conflicts:
        print("Conflicts detected:")
        for c in conflicts:
            print(f"{c.__class__.__name__} at {c.time}, teacher: {c.teacher.name}")
    else:
        print("No conflicts detected")
