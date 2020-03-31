from googleapiclient.errors import HttpError

from Course import Course
from Directory import get_user_email_from_id
import csv, os
from operator import itemgetter

def add_count(user, submitted, course, assignmentName, submission_count_dict):
    if user not in submission_count_dict.keys():
        submission_count_dict[user] = {'name': get_user_email_from_id(user),
                                       'complete': 0,
                                       'max': 0,
                                       'courses': [],
                                       'completed assignments': [],
                                       'missing assignments': []}
    if course not in submission_count_dict[user]['courses']:
        submission_count_dict[user]['courses'].append(course)
    if submitted == 1:
        submission_count_dict[user]['completed assignments'].append(assignmentName)
    if submitted == 0:
        submission_count_dict[user]['missing assignments'].append(assignmentName)
    submission_count_dict[user]['complete'] += submitted
    submission_count_dict[user]['max'] += 1
    return submission_count_dict

def sort_submission_count_dict(d):
    student_list = []
    for k, v in d.items():
        d[k]['percent done'] = v['complete'] / v['max']*100
        d[k]['courses'] = f'{" ".join(str(x) for x in d[k]["courses"])}'
        student_list.append(d[k])
    out_list = sorted(student_list, key=itemgetter('percent done', 'name'))
    return out_list


def main(teacherEmail):
    abelCourses = Course.get_teachers_courses(teacherEmail=teacherEmail)
    print('got courses')

    submission_count_dict = {}
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
                if a.submissions is not None:
                    for s in a.submissions:
                        try:
                            if s.state == 'TURNED_IN' or s.state == 'RETURNED':
                                submission_count_dict = add_count(user=s.studentId, submitted=1, course=course.name, assignmentName=a.title, submission_count_dict=submission_count_dict)
                            else:
                                submission_count_dict = add_count(user=s.studentId, submitted=0, course=course.name, assignmentName=a.title, submission_count_dict=submission_count_dict)
                        except HttpError:
                            continue


    dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir, 'output', f'{teacherEmail}.csv')
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'complete', 'max', 'percent done', 'courses', 'missing assignments', 'completed assignments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        sorted_students = sort_submission_count_dict(submission_count_dict)
        for student in sorted_students:
            writer.writerow(student)
    return filename

if __name__ == "__main__":
    main('angelinaulrich@springfield-schools.org')