from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from utils.schedule import LESSON_TIMES


@dataclass
class Session(ABC):
    name: str
    period_number: int
    room: int
    session_date: date

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string")

        if self.period_number not in LESSON_TIMES:
            raise ValueError(f"Lesson number {self.period_number} is invalid. Must be between 1 and 7.")

        if not isinstance(self.room, int) or self.room <= 0:
            raise ValueError("Room must be a positive integer")

        if not isinstance(self.session_date, date):
            raise TypeError("session_date must be a datetime.date instance")

    def get_time_range(self) -> tuple[str, str]:
        return LESSON_TIMES[self.period_number]

    @abstractmethod
    def per_form(self) -> None:
        pass
