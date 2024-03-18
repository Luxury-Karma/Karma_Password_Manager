import os.path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SCOPES = ['openid', "https://www.googleapis.com/auth/userinfo.profile",
                 'https://www.googleapis.com/auth/userinfo.email']

SERVER_BACK_UP_DIRECTORY_NAME: str = "ServerBackUp"
SERVER_BACK_FILE_NAME: str = "back_up.txt"
TEMP_FILE_TO_BACK_UP: str = 'D:\\projet\\back_up.txt'
SERVICE_ACCOUNT_FILE = "D:\\projet\\api_files\\sunlit-cove-417018-1246eeda431f.json"

def google_token_start():
    # Create credentials using the Service Account file
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If you need to impersonate a user, uncomment the following line and replace 'user@example.com' with the user's email
    # creds = creds.with_subject('user@example.com')

    return creds


def get_service() -> build:
    return build('drive', 'v3', credentials=google_token_start())


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
        media = MediaFileUpload(TEMP_FILE_TO_BACK_UP, mimetype='text/plain')
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File created!")
        return

    print("Updating the existing file.")
    media = MediaFileUpload(TEMP_FILE_TO_BACK_UP, mimetype='text/plain')
    service.files().update(fileId=file_id, media_body=media).execute()
    print("File updated!")


def download_file(service: build, file_id: str, local_dest: str) -> None:
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_dest, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    print("Download Complete!")


def print_all_files(service: build) -> None:
    items = get_files_and_id(service)
    for item in items:
        print(f"File Name: {item['name']}, File ID: {item['id']}")
