class Submission:
    def __init__(self, json):
        self.json = json
        self.courseId = self.json['courseId']
        self.assignmentId = self.json['courseWorkId']
        self.id = self.json['id']
        self.studentId = self.json['userId']
        self.state = self.json['state']
        self.lastUpdated = self.json['updateTime']
