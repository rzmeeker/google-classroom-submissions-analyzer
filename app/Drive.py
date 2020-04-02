from googleapiclient.discovery import MediaFileUpload
from app.service import get_drive_service


drive_service = get_drive_service()

def upload(file, email):
    file_metadata = {'name': email}
    media = MediaFileUpload(f'{file}',
                            mimetype='text/csv')
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')


def share(fileId, role, email):
    valid_roles = ['owner', 'organizer', 'fileOrganizer', 'writer', 'commenter', 'reader']
    if role not in valid_roles:
        role = 'reader'
    body = {'role': role,
            'type': 'user',
            'emailAddress': email}
    drive_service.permissions().create(fileId=fileId, body=body).execute()