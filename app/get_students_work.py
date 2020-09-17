from googleapiclient.errors import HttpError

from app.Course import Course
from app.Directory import get_user_email_from_id, get_names_from_email
import csv, os
from operator import itemgetter
from app.reports import *
from datetime import timedelta, date, datetime
from rfc3339 import rfc3339

def add_count(user, submitted, course, assignmentName, submission_count_dict):
    if user not in submission_count_dict.keys():
        mail = get_user_email_from_id(user)
        names = get_names_from_email(mail)
        submission_count_dict[user] = {'first': names.get('givenName'),
                                       'last': names.get('familyName'),
                                       'mail': mail,
                                       'complete': 0,
                                       'max': 0,
                                       'courses': [],
                                       'turned in assignments': [],
                                       'returned assignments': [],
                                       'missing assignments': []}
    if course not in submission_count_dict[user]['courses']:
        submission_count_dict[user]['courses'].append(course)
    if submitted == 2:
        submission_count_dict[user]['returned assignments'].append(assignmentName)
    if submitted == 1:
        submission_count_dict[user]['turned in assignments'].append(assignmentName)
    if submitted == 0:
        submission_count_dict[user]['missing assignments'].append(assignmentName)
    if submitted == 1 or submitted == 2:
        submission_count_dict[user]['complete'] += 1
    submission_count_dict[user]['max'] += 1
    return submission_count_dict

def sort_submission_count_dict(d):
    student_list = []
    for k, v in d.items():
        d[k]['percent done'] = v['complete'] / v['max']*100
        d[k]['courses'] = f'{" ".join(str(x) for x in d[k]["courses"])}'
        student_list.append(d[k])
    out_list = sorted(student_list, key=itemgetter('percent done', 'first', 'last'))
    return out_list

def add_meet_data_to_dict(service, student_dict, teacher_email):
    for student in student_dict:
        student_email = student.get('mail')
        shared_meetings = find_shared_meetings(service=service,
                                               teacher=teacher_email,
                                               student=student_email,
                                               startTime=179,
                                               endTime=-1)
        if shared_meetings is not None:
            student_meet_data = get_all_meet_results(service=service,
                                                     startTime=179,
                                                     endTime=-1,
                                                     userKey=student_email)
            meets_attended = []
            for meeting_code in shared_meetings:
                for meet in student_meet_data:
                    params = get_meet_params_from_json(meet)
                    if params.get('meeting_code') == meeting_code:
                        if params.get('duration') > 600:
                            meets_attended.append(f"{params.get('date').month}/{params.get('date').day}")
            sorted_meets_attended = sorted(meets_attended)
            meets_attended = []
            for meet in sorted_meets_attended:
                if meet not in meets_attended:
                    meets_attended.append(meet)
            student['Dates Meet Attended'] = sorted(meets_attended)
            student['Meets Attended'] = len(meets_attended)
        else:
            student['Dates Meet Attended'] = None
            student['Meets Attended'] = 0
    return student_dict



def get_meet_params_from_json(meeting_dict):
    duration = 0
    organizer_email = None
    meeting_code = None
    date = None
    time = meeting_dict.get('id').get('time')
    day = time.split('T')[0]
    date = datetime.strptime(day, "%Y-%m-%d").date()
    events = meeting_dict.get('events')
    if len(events) != 0:
        if events[0].get('parameters'):
            params = events[0].get('parameters')
            for param in params:
                if param.get('name') == 'duration_seconds':
                    duration = int(param.get('intValue'))
                if param.get('name') == 'organizer_email':
                    organizer_email = param.get('value')
                if param.get('name') == 'meeting_code':
                    meeting_code = param.get('value')
    meet_params = {
        'duration': duration,
        'organizer_email': organizer_email,
        'meeting_code': meeting_code,
        'date': date
    }
    return meet_params

def main(teacherEmail):
    abelCourses = Course.get_teachers_courses(teacherEmail=teacherEmail)
    #print('got courses')

    submission_count_dict = {}
    for course in abelCourses:
        if course.is_cached():
            pass
            #print(course.name, 'retrieved from cache')
        else:
            course.save_to_cache()
            #print(course.name, 'cached for next time!')
        if course.assignments is not None:
            if course.assignments_cached() is False:
                #print('Caching Assignments')
                course.cache_all_assignments()
            else:
                pass
                #print(f'Assignments already cached for {course.name}')
            for a in course.assignments:
                if a.submissions is not None:
                    for s in a.submissions:
                        try:
                            if s.state == 'RETURNED':
                                submission_count_dict = add_count(user=s.studentId, submitted=2, course=course.name, assignmentName=a.title, submission_count_dict=submission_count_dict)
                            if s.state == 'TURNED_IN':
                                submission_count_dict = add_count(user=s.studentId, submitted=1, course=course.name, assignmentName=a.title, submission_count_dict=submission_count_dict)
                            else:
                                submission_count_dict = add_count(user=s.studentId, submitted=0, course=course.name, assignmentName=a.title, submission_count_dict=submission_count_dict)
                        except HttpError:
                            continue

    sorted_students = sort_submission_count_dict(submission_count_dict)
    reports_service = service.get_reports_service()
    add_meet_data_to_dict(service=reports_service,
                          student_dict=sorted_students,
                          teacher_email=teacherEmail)

    dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(dir, 'output', f'{teacherEmail}.csv')
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['first', 'last', 'mail', 'complete', 'max', 'percent done', 'courses', 'missing assignments', 'turned in assignments', 'returned assignments', 'Meets Attended', 'Dates Meet Attended']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for student in sorted_students:
            writer.writerow(student)
    return filename

if __name__ == "__main__":
    pass