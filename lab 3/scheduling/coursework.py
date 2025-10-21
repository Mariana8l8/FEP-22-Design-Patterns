class CourseWork:
    def __init__(self, supervisor):
        self.supervisor = supervisor

class OnlineSubmission(CourseWork):
    def submit(self, file_path):
        self.file_path = file_path
        return True

class GitHubSubmission(CourseWork):
    def submit(self, repo_link):
        self.repo_link = repo_link
        return True

class OralDefense(CourseWork):
    def submit(self, date):
        self.date = date
        return True
