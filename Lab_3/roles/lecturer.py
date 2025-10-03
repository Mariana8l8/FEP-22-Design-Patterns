from __future__ import annotations
from dataclasses import dataclass, field

from roles.teacher import Teacher
from sessions.lecture import Lecture


@dataclass
class Lecturer(Teacher):
    completed_lectures: list[Lecture] = field(default_factory=list, init=False)

    def per_form(self, lecture: Lecture) -> None:
        if not isinstance(lecture, Lecture):
            raise TypeError("Lecture must be of type Lecture")

        lecture.per_form()
        self.completed_lectures.append(lecture)
        self.num_sessions_completed += 1
