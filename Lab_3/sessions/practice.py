from __future__ import annotations
from datetime import date
from utils.schedule import LESSON_TIMES

from sessions.session import Session
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from roles.assistant import Assistant


class Practice(Session):
    OCCUPIED_ROOMS: list[tuple[int, int, date]] = []

    def __init__(self, name: str, period_number: int, room: int, session_date: date, assistant: Assistant) -> None:
        super().__init__(name, period_number, room, session_date)
        from roles.assistant import Assistant
        if not isinstance(assistant, Assistant):
            raise TypeError("Assistant must be an instance of Assistant")

        self.assistant = assistant

        key = (self.room, self.period_number, self.session_date)
        if key in Practice.OCCUPIED_ROOMS:
            raise ValueError(f"Room {self.room} is already occupied for period {self.period_number}")

        Practice.OCCUPIED_ROOMS.append(key)

    def per_form(self) -> None:
        start, end = LESSON_TIMES[self.period_number]
        print(f"Practice '{self.name}' from {start} to {end} in room {self.room}, "
              f"conducted by {self.assistant.name}")
