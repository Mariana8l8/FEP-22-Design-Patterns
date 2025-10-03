from __future__ import annotations
from datetime import date

from factories.session_factory import SessionFactory
from roles.assistant import Assistant
from sessions.practice import Practice


class PracticeFactory(SessionFactory):
    def create(self, session_data: tuple[tuple[int, int, date], ...], assistant: Assistant) -> list[Practice]:
        return [
            Practice(f'Practice {i}', period_number, room, session_date, assistant)
            for i, (period_number, room, session_date) in enumerate(session_data, start=1)
        ]