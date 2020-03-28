from Course import Course
from Directory import get_user_email_from_id

abelCourses = Course.get_teachers_courses(teacherEmail='seanabel@springfield-schools.org')
print('got courses')

for course in abelCourses:
    if course.is_cached():
        print(course.name, 'retrieved from cache')
    else:
        course.save_to_cache()
        print(course.name, 'saved to cache for next time!')
    if course.assignments is not None:
        for assignment in course.assignments:
            submissions = course.get_submissions(assignment['id'])
            for submission in submissions:
                print(f"For assignment:{assignment['title']} in course: {course.name}")
                print(f"{get_user_email_from_id(submission['userId'])} has state {submission['state']}")
            input('Press Enter for next assignment')



    input('Press Enter for next course')