from scheduling.sessions import LectureSession, PracticalSession

class SessionFactory:
    def create_session(self, **kwargs):
        raise NotImplementedError

class LectureFactory(SessionFactory):
    def create_session(self, time, room, teacher):
        return LectureSession(time, room, teacher)

class PracticalFactory(SessionFactory):
    def create_session(self, time, room, teacher):
        return PracticalSession(time, room, teacher)
