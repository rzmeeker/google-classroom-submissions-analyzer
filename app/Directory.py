from googleapiclient.errors import HttpError
from app.service import get_directory_service

service = get_directory_service()

def get_user_email_from_id(id):
    try:
        result = service.users().get(userKey=id).execute()
        return result['primaryEmail']
    except HttpError:
        return 'No Longer Enrolled at Springfield Schools'

def get_names_from_email(email):
    try:
        result = service.users().get(userKey=email).execute()
        return result.get('name')
    except HttpError:
        return {
            'givenName': 'ERROR: Could not find user',
            'familyName': 'ERROR: Could not find user',
        }