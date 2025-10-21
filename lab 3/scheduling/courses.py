from scheduling.factories import LectureFactory, PracticalFactory
from scheduling.coursework import OnlineSubmission, GitHubSubmission, OralDefense

class CourseFactory:
    def create_lecture(self, **kwargs):
        raise NotImplementedError
    def create_practical(self, **kwargs):
        raise NotImplementedError
    def create_coursework(self, **kwargs):
        raise NotImplementedError

class ProgrammingCourseFactory(CourseFactory):
    def create_lecture(self, time, room, teacher):
        return LectureFactory().create_session(time, room, teacher)
    def create_practical(self, time, room, teacher):
        return PracticalFactory().create_session(time, room, teacher)
    def create_coursework(self, mentor):
        return OnlineSubmission(mentor)

class DatabasesCourseFactory(CourseFactory):
    def create_lecture(self, time, room, teacher):
        return LectureFactory().create_session(time, room, teacher)
    def create_practical(self, time, room, teacher):
        return PracticalFactory().create_session(time, room, teacher)
    def create_coursework(self, mentor):
        return GitHubSubmission(mentor)
