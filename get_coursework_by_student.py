from service import get_classroom_service
from Directory import get_user_email_from_id
from pprint import pprint


def get_all_courses(service):
    return None

def get_coursework(course_id):
    results = service.courses().courseWork().list(courseId=course_id, pageSize=10, orderBy="dueDate desc").execute()
    assignments = results.get('couseWork', [])
    for assignment in assignments:
        print(assignment)


service = get_classroom_service()
#print(service.courses().courseWork().list(courseId=56998666011))

results = service.courses().list(teacherId="seanabel@springfield-schools.org").execute()
courses = results['courses']
for course in courses:
    courseId = course['id']
    #pprint(course)
    assignments = service.courses().courseWork().list(courseId=courseId).execute()
    if assignments:
        for assignment in assignments['courseWork']:
            #pprint(assignment)
            assignmentId = assignment['id']
            studentSubmissions = service.courses().courseWork().studentSubmissions().list(courseId=courseId,
                                                                                  courseWorkId=assignmentId).execute()
            #pprint(studentSubmissions)
            for submission in studentSubmissions['studentSubmissions']:
                print(f"For assignment:{assignment['title']} in course: {course['name']}")
                print(f"{get_user_email_from_id(submission['userId'])} has state {submission['state']}")
    input('Press Enter to load Next Class')

'''
results = service.courses().list(pageSize=20).execute()
courses = results.get('courses', [])
for course in courses:
    #print(course['name'], course['id'])
    #print(course)
    course_id = course['id']
    teacher_query = service.courses().teachers().list(courseId=course_id).execute()
    print(teacher_query)
    teacher_id = teacher_query['teachers'][0]['profile']['id']
    get_teacher_query = service.courses().teachers().get(courseId=course_id, userId=teacher_id).execute()
    print(get_teacher_query)
    #get_coursework(course_id)'''