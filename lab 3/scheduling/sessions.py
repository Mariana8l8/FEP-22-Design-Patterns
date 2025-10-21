class ClassSession:
    def __init__(self, time, room, teacher):
        self.time = time
        self.room = room
        self.teacher = teacher

class LectureSession(ClassSession):
    pass

class PracticalSession(ClassSession):
    pass