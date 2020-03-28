from service import get_classroom_service
import os
import json
from Submission import Submission

class Assignment:

    classroom_service = get_classroom_service()

    def __init__(self, assignmentId):
        self.id = str(assignmentId)
        self.service = Assignment.classroom_service
        self.json = self.get_json()
        self.courseId = self.json['courseId']
        self.submissions = self.get_submissions()


    def get_json(self):
        if self.is_cached():
            with open(self.is_cached(), 'r') as jsonfile:
                print(f'Retrieved assignment from cache: {self.id}')
                return json.load(jsonfile)
        else:
            assignments_packed = self.service.courses().courseWork().get(courseId=self.id, id=self.id).execute()
            if assignments_packed != {}:
                print(assignments_packed)
            else:
                return None

    def is_cached(self):
        dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache', 'assignments')
        for root, dirs, files in os.walk(dir):
            for name in files:
                if self.id in name:
                    print(f'Found cached as {name}')
                    return os.path.join(root, name)
        print(f'Assignment {self.id}: Not found in cache')
        return False

    def get_submissions(self):
        print('getting submissions')
        studentSubmissions = self.service.courses().courseWork().studentSubmissions().list(courseId=self.courseId,
                                                                                      courseWorkId=self.id).execute()
        submissions_list = studentSubmissions['studentSubmissions']
        submissions = []
        for s in submissions_list:
            submissions.append(Submission(s))
        return submissions