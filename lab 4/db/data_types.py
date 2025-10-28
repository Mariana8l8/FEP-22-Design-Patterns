class DataType:
    def validate(self, value):
        return True

class IntegerType(DataType):
    def validate(self, value):
        return isinstance(value, int) or value is None

class StringType(DataType):
    def __init__(self, max_length=None):
        self.max_length = max_length
    def validate(self, value):
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        if self.max_length and len(value) > self.max_length:
            return False
        return True

class BooleanType(DataType):
    def validate(self, value):
        return isinstance(value, bool) or value is None

class DateType(DataType):
    def validate(self, value):
        from datetime import date
        return isinstance(value, date) or value is None