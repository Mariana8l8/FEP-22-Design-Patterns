class Column:
    def __init__(self, name, data_type, nullable=True, primary_key=False, foreign_key=None):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.foreign_key = foreign_key

    def validate(self, value):
        if value is None and not self.nullable:
            return False
        return self.data_type.validate(value)
