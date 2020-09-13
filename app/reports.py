from app import service
from googleapiclient.discovery import Resource
from datetime import timedelta, date, datetime
from rfc3339 import rfc3339



def get_all_meet_results(service: Resource, startTime: int, endTime: int=None, userKey: str='all'):
    if endTime == None:
        rfcEndTime = get_rfc_datetime_for_x_days_ago(startTime-1)
    else:
        rfcEndTime = get_rfc_datetime_for_x_days_ago(endTime)
    rfcStartTime = get_rfc_datetime_for_x_days_ago(startTime)
    page_token = 'Dummy'
    results = []
    while page_token is not None:
        result = service.activities().list(applicationName='meet',
                                           userKey=userKey,
                                           startTime=rfcStartTime,
                                           endTime=rfcEndTime).execute()
        if result.get('items'):
            for item in result.get('items', None):
                results.append(item)
        page_token = result.get('nextPageToken', None)
    return results


def get_meeting_participants(results):
    out_dict = {}
    for result in results:
        email = result.get('actor').get('email')
        if email is not None:
            params = result.get('events')[0].get('parameters')
            for param in params:
                if param.get('name') == 'meeting_code':
                    meeting = param.get('value')
                    if meeting in out_dict.keys():
                        if email not in out_dict[meeting]:
                            out_dict[meeting].append(email)
                    else:
                        out_dict[meeting] = [email]
    return out_dict

def get_rfc_datetime_for_x_days_ago(days_ago: int):
    today = date.today()
    target_day = today - timedelta(days=days_ago)
    return rfc3339(target_day)

def did_user_attend_meeting_with(user, other_user, meetings):
    for meeting, participants in meetings.items():
        for participant in participants:
            if user.lower() == participant.lower():
                for participant in participants:
                    if other_user.lower() == participant.lower():
                        return True
    return False


def user_attended_meetings_with(user, meetings):
    out_list = []
    for meeting, participants in meetings.items():
        for participant in participants:
            if participant.lower() == user.lower():
                for participant in participants:
                    out_list.append(participant)
    while user in out_list:
        out_list.remove(user)
    return out_list


def find_shared_meetings(service: Resource, teacher: str, student: str, startTime: int, endTime: int):
    shared_meetings = []
    results = get_all_meet_results(service=service,
                                   startTime=startTime,
                                   endTime=endTime,
                                   userKey=teacher)
    results2 = get_all_meet_results(service=service,
                                    startTime=startTime,
                                    endTime=endTime,
                                    userKey=student)
    meetings = get_meeting_participants(results)
    meetings2 = get_meeting_participants(results2)
    for meeting_code in meetings.keys():
        if meeting_code in meetings2.keys():
            shared_meetings.append(meeting_code)
    if shared_meetings:
        return shared_meetings
    return None



if __name__ == "__main__":
    service = service.get_reports_service()
    #days_ago = 2  #changeme if you want a report for X days in the past.
    shared_meetings = find_shared_meetings(service=service,
                                           teacher='robertmeeker@springfield-schools.org',
                                           student='StephanieMahoney@springfield-schools.org',
                                           startTime=30,
                                           endTime=0)
    print('foo')

    '''
    yesterday_results = get_all_meet_results(service=service,
                                             startTime=1,
                                             endTime=0)
    yesterday_meetings = get_meeting_participants(yesterday_results)

    for meeting, participants in meetings.items():
        print(f"Meeting ID: {meeting} had the participants: {participants}")

    print('Did I attend a meeting with Cory?')
    print(did_user_attend_meeting_with('robertmeeker@springfield-schools.org', 'corycantu@springfield-schools.org', meetings))
    print("Did I attend a meeting with potato?")
    print(did_user_attend_meeting_with('robertmeeker@springfield-schools.org', 'potato@springfield-schools.org',
                                       meetings))
    print("Did I attend a meeting with Kristie Chandler?")
    print(did_user_attend_meeting_with('robertmeeker@springfield-schools.org', 'KristieChandler@springfield-schools.org',
                                       meetings))
    print("Who did I attend meetings with today?")
    print(user_attended_meetings_with('robertmeeker@springfield-schools.org', meetings))
    print("What about yesterday?")
    print(user_attended_meetings_with('robertmeeker@springfield-schools.org', yesterday_meetings))

    for i in range(0, 7):
        old_results = get_all_meet_results(service=service,
                                           startTime=i,
                                           endTime=i-1)
        old_meetings = get_meeting_participants(old_results)
        print(f'He attended meetings with {i} days ago:')
        print(user_attended_meetings_with('robertmeeker@springfield-schools.org', old_meetings))
    '''