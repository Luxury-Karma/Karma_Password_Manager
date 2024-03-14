import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

SERVER_BACK_UP_DIRECTORY_NAME: str = "ServerBackUp"
SERVER_BACK_FILE_NAME: str = "file.txt"


def google_token_start():
    """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("../token.json"):
        creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "D:\\projet\\api_files\\secret_token.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../token.json", "w") as token:
            token.write(creds.to_json())


def get_token_connection() -> Credentials:
    return Credentials.from_authorized_user_file("../token.json", SCOPES)


def get_service() -> build:
    return build('drive', 'v3', credentials=get_token_connection())


def get_files_and_id(service: build) -> dict:

    # Appelez la méthode files().list() du service Drive v3.
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    return items


def get_server_backup_directory(list_directory:dict, service: build):
    server_b_id = ""
    for e in list_directory:
        if e["name"] == SERVER_BACK_UP_DIRECTORY_NAME:
            server_b_id = e["id"]
            break

    if server_b_id == "":
        print("back up directory not found")
        folder_metadata = {
            'name': f'{SERVER_BACK_UP_DIRECTORY_NAME}',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        server_b_id = folder.get('id')
    return server_b_id


def get_server_backup_file(items):
    file_id = None
    for item in items:
        if item['name'] == SERVER_BACK_FILE_NAME:
            print(f"{SERVER_BACK_FILE_NAME} already exists in the directory.")
            file_id = item['id']
            break
    return file_id


def update_backup(list_directory:dict, service: build) -> None:

    server_b_id = get_server_backup_directory(list_directory, service)

    results = service.files().list(
        q=f"'{server_b_id}' in parents",
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    file_id = get_server_backup_file(items)

    if file_id is None:
        print("File not found. Creating it.")
        file_metadata = {'name': f'{SERVER_BACK_FILE_NAME}', 'parents': [f'{server_b_id}']}
        media = MediaFileUpload("D:\\projet\\apps\\test.txt", mimetype='text/plain')
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created!")
        return

    print("Updating the existing file.")
    media = MediaFileUpload("D:\\projet\\apps\\test.txt", mimetype='text/plain')
    service.files().update(fileId=file_id, media_body=media).execute()
    print("File updated!")

