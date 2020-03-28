from service import get_directory_service

service = get_directory_service()

def get_user_email_from_id(id):
    result = service.users().get(userKey=id).execute()
    return result['primaryEmail']


get_user_email_from_id('111312513926432543114')