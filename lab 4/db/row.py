class Row:
    def __init__(self, data):
        self.data = data
        self.id = None

    def __getitem__(self, column_name):
        return self.data.get(column_name)

    def __setitem__(self, column_name, value):
        self.data[column_name] = value

    def keys(self):
        return self.data.keys()
