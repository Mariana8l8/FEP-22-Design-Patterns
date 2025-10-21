class StudentGroup:
    def __init__(self, name):
        self.name = name
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def check_conflicts(self):
        conflicts = []
        times = {}
        for s in self.sessions:
            if s.time in times:
                conflicts.append(s)
            else:
                times[s.time] = s
        return conflicts

    def enroll(self, course_factory, lecture_teacher, practical_teacher, mentor):
        lecture = course_factory.create_lecture(time="Wed 15:05", room="129", teacher=lecture_teacher)
        practical = course_factory.create_practical(time="Mon 13:30", room="#3", teacher=practical_teacher)
        coursework = course_factory.create_coursework(mentor=mentor)
        self.add_session(lecture)
        self.add_session(practical)
        return coursework
