from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional


class DataType(ABC):
    @abstractmethod
    def validate(self, value) -> bool:
        pass

    @abstractmethod
    def convert(self, value):
        pass


class IntegerType(DataType):
    def validate(self, value) -> bool:
        return isinstance(value, int)

    def convert(self, value) -> Optional[int]:
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert value '{value}' to IntegerType")


class StringType(DataType):
    def validate(self, value) -> bool:
        return isinstance(value, str)

    def convert(self, value) -> Optional[str]:
        if value is None:
            return None
        try:
            return str(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert value '{value}' to StringType")


class BooleanType(DataType):
    TRUE_VALUES = {"true", "1", "yes", "y", "t"}
    FALSE_VALUES = {"false", "0", "no", "n", "f"}

    def validate(self, value) -> bool:
        return isinstance(value, bool)

    def convert(self, value) -> Optional[bool]:
        if value is None:
            return None
        if self.validate(value):
            return value
        if isinstance(value, int):
            return bool(value)
        if isinstance(value, str):
            v = value.strip().lower()
            if v in self.TRUE_VALUES:
                return True
            if v in self.FALSE_VALUES:
                return False
            raise ValueError(f"Cannot convert string '{value}' to BooleanType")
        raise TypeError(f"Unsupported type for BooleanType conversion: {type(value).__name__}")


class DateType(DataType):
    FORMATS = ["%Y.%m.%d", "%Y-%m-%d"]

    def validate(self, value) -> bool:
        return isinstance(value, date)

    def convert(self, value) -> Optional[date]:
        if value is None:
            return None
        if self.validate(value):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            for fmt in self.FORMATS:
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            raise ValueError(
                f"Cannot convert string '{value}' to DateType (expected formats: {', '.join(self.FORMATS)})"
            )
        raise TypeError(f"Unsupported type for DateType conversion: {type(value).__name__}")
