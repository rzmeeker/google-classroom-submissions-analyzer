from app.service import get_classroom_service
import os
import json
from app.Assignment import Assignment
from app.Directory import get_user_email_from_id

class Course:

    classroom_service = get_classroom_service()

    def __init__(self, courseId):
        self.id = str(courseId)
        self.service = Course.classroom_service
        self.json = self.get_json()
        self.name = self.json['name']
        self.teacherID = self.json['ownerId']
        self.teacherEmail = get_user_email_from_id(self.teacherID)
        self.assignments = self.get_assignments()



    def get_assignments(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        course_dir = os.path.join(dir, 'cache', 'assignments', f'{self.id}')
        print(f'getting assignments for {self.name} with primary teacher {self.teacherEmail}')
        if self.assignments_cached() == False:
            assignments_packed = self.service.courses().courseWork().list(courseId=self.id).execute()
            if assignments_packed != {}:
                assignments = assignments_packed['courseWork']
                return assignments
            else:
                print(f'Found No Assignments for course {self.name}:{self.id}')
                return None
        else:
            assignments = []
            #print(f'Found Cache for Course: {self.id}')
            f = []
            for (dirpath, dirnames, filenames) in os.walk(course_dir):
                f.extend(filenames)
                for file in f:
                    withoutExtension = file.split('.')[0]
                    assignments.append(Assignment(withoutExtension))
            return assignments

    def assignments_cached(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        course_dir = os.path.join(dir, 'cache', 'assignments', f'{self.id}')
        if os.path.exists(course_dir):
            #todo: check if cache recent
            return True
        else:
            return False


    def cache_all_assignments(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        course_dir = os.path.join(dir, 'cache', 'assignments', f'{self.id}')
        if not os.path.exists(course_dir):
            os.mkdir(course_dir)
        if self.assignments is None:
            pass
        else:
            for assignment in self.assignments:
                filename = os.path.join(dir, 'cache', 'assignments', f'{self.id}', f'{assignment["id"]}.json')
                with open(filename, 'w') as jsonfile:
                    json.dump(assignment, jsonfile)
        self.assignments = self.get_assignments()


    def is_cached(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir, 'cache', 'courses', f'{self.id}.json')
        if os.path.exists(filename):
            return True
        else:
            return False

    def save_to_cache(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir, 'cache', 'courses', f'{self.id}.json')
        with open(filename, 'w') as jsonfile:
            json.dump(self.json, jsonfile)

    def get_json(self):
        if self.is_cached():
            dir = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir, 'cache', 'courses', f'{self.id}.json')
            with open(filename, 'r') as jsonfile:
                return json.load(jsonfile)
        else:
            return self.service.courses().get(id=self.id).execute()

    @classmethod
    def get_teachers_courses(cls, teacherEmail):
        out_courses = []
        results = cls.classroom_service.courses().list(teacherId=teacherEmail, courseStates='ACTIVE').execute()
        courses = results['courses']
        for course in courses:
            print(f"Found Course: {course['id']} for {teacherEmail}")
            out_courses.append(Course(course['id']))
        return out_courses