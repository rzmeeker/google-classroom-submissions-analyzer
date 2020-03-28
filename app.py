from Course import Course
from Directory import get_user_email_from_id
import csv, os

teacherEmail='seanabel@springfield-schools.org'
abelCourses = Course.get_teachers_courses(teacherEmail=teacherEmail)
print('got courses')

submission_count_dict = {}

def add_count(user, submitted):
    if user not in submission_count_dict.keys():
        submission_count_dict[user] = {'name': get_user_email_from_id(submission['userId']),
                                       'complete': 0,
                                       'max': 0}
    submission_count_dict[user]['complete'] += submitted
    submission_count_dict[user]['max'] += 1



for course in abelCourses:
    if course.is_cached():
        print(course.name, 'retrieved from cache')
    else:
        course.save_to_cache()
        print(course.name, 'saved to cache for next time!')
    if course.assignments is not None:
        if course.assignments_cached() is False:
            print('Assignments being cached now.')
            course.cache_all_assignments()
        else:
            print('Assignments already cached.')
        for assignment in course.assignments:
            #print(assignment)
            print(assignment['id'])
            submissions = course.get_submissions(assignment['id'])
            for submission in submissions:
                #print(f"For assignment:{assignment['title']} in course: {course.name}")
                #print(f"{get_user_email_from_id(submission['userId'])} has state {submission['state']}")
                if submission['state'] == 'TURNED_IN' or submission['state'] == 'RETURNED':
                    add_count(user=submission['userId'], submitted=1)
                else:
                    add_count(user=submission['userId'], submitted=0)
            #input('Press Enter for next assignment')



    #input('Press Enter for next course')

dir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir, 'output', f'{teacherEmail}.csv')
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['name', 'complete', 'max']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for student in submission_count_dict.keys():
        print(submission_count_dict[student])
        writer.writerow(submission_count_dict[student])