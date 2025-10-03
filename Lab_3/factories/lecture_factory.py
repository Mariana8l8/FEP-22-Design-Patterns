from __future__ import annotations
from datetime import date

from factories.session_factory import SessionFactory
from roles.lecturer import Lecturer
from sessions.lecture import Lecture


class LectureFactory(SessionFactory):
    def create(self, session_data: tuple[tuple[int, int, date], ...], lecturer: Lecturer) -> list[Lecture]:
        return [
            Lecture(f'Lecture {i}', period_number, room, session_date, lecturer)
            for i, (period_number, room, session_date) in enumerate(session_data, start=1)
        ]
