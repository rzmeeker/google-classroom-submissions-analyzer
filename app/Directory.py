from googleapiclient.errors import HttpError
from app.service import get_directory_service

service = get_directory_service()

def get_user_email_from_id(id):
    try:
        result = service.users().get(userKey=id).execute()
        return result['primaryEmail']
    except HttpError:
        return 'No Longer Enrolled at Springfield Schools'