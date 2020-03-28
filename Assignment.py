from service import get_classroom_service
import os
import json

class Assignment:

    classroom_service = get_classroom_service()

    def __init__(self, assignmentId):
        self.id = assignmentId
        self.json = self.get_json()


    def get_json(self):
        if self.is_cached():
            dir = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir, 'cache', 'assignments', f'{self.id}.json')
            with open(filename, 'r') as jsonfile:
                print(f'Retrieved assignment from cache: {self.id}')
                return json.load(jsonfile)
        else:
            assignments_packed = self.service.courses().courseWork().get(courseId=self.id, id=self.id).execute()
            if assignments_packed != {}:
                print(assignments_packed)
            else:
                return None