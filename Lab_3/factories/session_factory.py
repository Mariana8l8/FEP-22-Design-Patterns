from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date

from roles.teacher import Teacher
from sessions.session import Session


class SessionFactory(ABC):
    @abstractmethod
    def create(self, session_data: tuple[tuple[int, int, date], ...], teacher: Teacher) -> list[Session]:
        pass
