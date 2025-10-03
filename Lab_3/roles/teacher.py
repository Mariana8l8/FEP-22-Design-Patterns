from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from sessions.session import Session
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from courses.course import Course


@dataclass
class Teacher(ABC):
    name: str
    course: Course = field(init=False)
    num_sessions_completed: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string")

    @abstractmethod
    def per_form(self, session: Session) -> None:
        pass
