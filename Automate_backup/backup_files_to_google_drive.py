import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Replace with your own values
SAVE_FOLDER_PATH = "C:\\Users\\aadit\\Documents\\Python_assignments\\Automate_backup\\local_backup\\"
CREDENTIALS_FILE = "credentials.json"   # Your private credentials file

# Replace 'YOUR_FOLDER_ID' with the actual ID of the folder you want to use on Google Drive
YOUR_FOLDER_ID = '1CdQmFd2yahVZhkZF5OWWlcZyv2zQqZk5'

# Google Drive API settings
SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"

# Authenticate using the Google Drive API
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Create the Google Drive API client
service = build("drive", "v3", credentials=creds)

# Helper function to upload a file to Google Drive
def upload_drive_file(local_path, drive_folder_id):
    file_metadata = {
        "name": os.path.basename(local_path),
        "parents": [drive_folder_id]
    }
    media = MediaFileUpload(local_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"File ID: {file.get('id')}")
    return file.get("id")

# Uploading the file sequentially from the backup folder
for root, dirs, files in os.walk(SAVE_FOLDER_PATH):
    for file in files:
        local_file_path = os.path.join(root, file)
        relative_path = os.path.relpath(local_file_path, SAVE_FOLDER_PATH)

        # Upload the file onto Google Drive
        print(f"Uploading {relative_path} to Google Drive")
        upload_drive_file(local_file_path, YOUR_FOLDER_ID)
