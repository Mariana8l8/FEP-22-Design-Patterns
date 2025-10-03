from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field

from roles.assistant import Assistant
from roles.lecturer import Lecturer
from sessions.lecture import Lecture
from sessions.practice import Practice


@dataclass
class Course(ABC):
    name: str
    lecturer: Lecturer
    assistant: Assistant
    future_lectures: list[Lecture]
    future_practices: list[Practice]
    completed_lectures: list[Lecture] = field(default_factory=list, init=False)
    completed_practices: list[Practice] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Course name must be a non-empty string")

        if not isinstance(self.lecturer, Lecturer):
            raise TypeError("lecturer must be an instance of Lecturer")

        if not isinstance(self.assistant, Assistant):
            raise TypeError("assistant must be an instance of Assistant")

        if not isinstance(self.future_lectures, list):
            raise TypeError("lectures must be a list of Lecture instances")
        for lecture in self.future_lectures:
            if not isinstance(lecture, Lecture):
                raise TypeError("Each item in lectures must be a Lecture instance")

        if not isinstance(self.future_practices, list):
            raise TypeError("practices must be a list of Practice instances")
        for practice in self.future_practices:
            if not isinstance(practice, Practice):
                raise TypeError("Each item in practices must be a Practice instance")

        self.lecturer.course = self
        self.assistant.course = self

    def complete_lecture(self, lecture: Lecture, group_name: str) -> None:
        if lecture in self.future_lectures:
            self.future_lectures.remove(lecture)
            self.completed_lectures.append(lecture)
            print(f"Group '{group_name}' attended lecture '{lecture.name}'")

    def complete_practice(self, practice: Practice, group_name: str) -> None:
        if practice in self.future_practices:
            self.future_practices.remove(practice)
            self.completed_practices.append(practice)
            print(f"Group '{group_name}' attended practice '{practice.name}'")
