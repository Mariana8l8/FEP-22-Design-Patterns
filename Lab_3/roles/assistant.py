from __future__ import annotations
from dataclasses import dataclass, field

from roles.teacher import Teacher
from sessions.practice import Practice


@dataclass
class Assistant(Teacher):
    completed_practices: list[Practice] = field(default_factory=list, init=False)

    def per_form(self, practice: Practice) -> None:
        if not isinstance(practice, Practice):
            raise TypeError("Practice must be of type Practice")

        practice.per_form()
        self.completed_practices.append(practice)
        self.num_sessions_completed += 1
