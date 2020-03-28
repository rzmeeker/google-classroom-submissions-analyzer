from Course import Course
from Directory import get_user_email_from_id
import csv, os

teacherEmail='seanabel@springfield-schools.org'
abelCourses = Course.get_teachers_courses(teacherEmail=teacherEmail)
print('got courses')

submission_count_dict = {}

def add_count(user, submitted):
    if user not in submission_count_dict.keys():
        submission_count_dict[user] = {'name': get_user_email_from_id(user),
                                       'complete': 0,
                                       'max': 0}
    submission_count_dict[user]['complete'] += submitted
    submission_count_dict[user]['max'] += 1


for course in abelCourses:
    if course.is_cached():
        print(course.name, 'retrieved from cache')
    else:
        course.save_to_cache()
        print(course.name, 'cached for next time!')
    if course.assignments is not None:
        if course.assignments_cached() is False:
            print('Caching Assignments')
            course.cache_all_assignments()
        else:
            print(f'Assignments already cached for {course.name}')
        for a in course.assignments:
            for s in a.submissions:
                if s.state == 'TURNED_IN' or s.state == 'RETURNED':
                    add_count(user=s.studentId, submitted=1)
                else:
                    add_count(user=s.studentId, submitted=0)



dir = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir, 'output', f'{teacherEmail}.csv')
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['name', 'complete', 'max']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for student in submission_count_dict.keys():
        print(submission_count_dict[student])
        writer.writerow(submission_count_dict[student])