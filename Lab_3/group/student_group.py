from __future__ import annotations
from dataclasses import dataclass, field
from typing import Type

from courses.course import Course
from sessions.lecture import Lecture
from sessions.practice import Practice
from sessions.session import Session


@dataclass
class StudentGroup:
    name: str
    courses: list[Course] = field(default_factory=list, init=False)
    current_sessions: dict[str, int] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string")

    def enroll(self, course: Course) -> None:
        if not isinstance(course, Course):
            raise TypeError("Course must be a Course")

        self.courses.append(course)

    def show_course_progress(self, course_name: str) -> None:
        course = next((c for c in self.courses if c.name == course_name), None)
        if not course:
            print(f"No course named '{course_name}' found in this group")
            return

        if not course.completed_lectures and not course.completed_practices:
            print(f"Course {course.name} has no completed sessions yet")
            return

        if not course.future_lectures and not course.future_practices:
            print(f"Course {course.name} is fully completed!")
            return

        print(f"Progress for course {course.name}:")
        if course.completed_lectures:
            print(f"  Completed lectures: {[lec.name for lec in course.completed_lectures]}")
        if course.future_lectures:
            print(f"  Remaining lectures: {[lec.name for lec in course.future_lectures]}")

        if course.completed_practices:
            print(f"  Completed practices: {[pr.name for pr in course.completed_practices]}")
        if course.future_practices:
            print(f"  Remaining practices: {[pr.name for pr in course.future_practices]}")

    def attend_session(self, course_name: str, session: Session) -> None:
        if self.current_sessions:
            print(f"Group '{self.name}' is already attending another session at this time")
            return

        course = next((c for c in self.courses if c.name == course_name), None)
        if not course:
            print(f"No course named '{course_name}' found in this group")
            return

        session_number = int(session.name.split()[1])

        if isinstance(session, Lecture):
            last_completed = int(course.completed_lectures[-1].name.split()[1]) if course.completed_lectures else 0
            if session_number != last_completed + 1:
                if last_completed == 0:
                    print(f"You must start with Lecture 1")
                elif session_number <= last_completed:
                    print(f"Lecture {session_number} has already been completed")
                else:
                    print(f"You must attend Lecture {last_completed + 1} before Lecture {session_number}")
                return

            course.complete_lecture(session, self.name)
            self.current_sessions[course_name] = session_number
            return

        if isinstance(session, Practice):
            last_completed = int(course.completed_practices[-1].name.split()[1]) if course.completed_practices else 0
            if session_number != last_completed + 1:
                if last_completed == 0:
                    print(f"You must start with Practice 1")
                elif session_number <= last_completed:
                    print(f"Practice {session_number} has already been completed")
                else:
                    print(f"You must attend Practice {last_completed + 1} before Practice {session_number}")
                return

            course.complete_practice(session, self.name)
            self.current_sessions[course_name] = session_number
            return

        print(f"Unknown session type for '{session.name}'")

    def leave_session(self, course_name: str) -> None:
        course = next((c for c in self.courses if c.name == course_name), None)
        if not course:
            print(f"No course named '{course_name}' found in this group")
            return

        if course_name not in self.current_sessions:
            print(f"Group '{self.name}' is not currently attending a session for course '{course_name}'")
            return

        session_number = self.current_sessions.pop(course_name)
        print(f"Group '{self.name}' has left session {session_number} of course '{course_name}'")


