#for use in RAG SYTEM to load drive add credentials.json
import os
import io
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveLoader:
    def __init__(self, credentials_path='credentials.json', token_path='token.pickle'):
        self.creds = None
        self.service = None
        self.credentials_path = credentials_path
        self.token_path = token_path
        self._authenticate()

    def _authenticate(self):
        """Authenticates the user with Google Drive API."""
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if os.path.exists(self.credentials_path):
                     # Check if it's a service account or client secret
                    try:
                        self.creds = Credentials.from_service_account_file(
                            self.credentials_path, scopes=SCOPES)
                    except ValueError:
                        # Assume it's a client secret for OAuth
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, SCOPES)
                        self.creds = flow.run_local_server(port=0)
                else:
                    raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}")

            # Save the credentials for the next run (only if not service account)
            if not isinstance(self.creds, Credentials): # Service account creds don't need pickling usually
                 with open(self.token_path, 'wb') as token:
                    pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)

    def download_file(self, file_id, output_path):
        """Downloads a file from Google Drive."""
        request = self.service.files().get_media(fileId=file_id)
        
        # Get file metadata to check name if needed, or just trust output_path
        # file_meta = self.service.files().get(fileId=file_id).execute()
        
        fh = io.FileIO(output_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f"Downloading file ID: {file_id} to {output_path}...")
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        print("Download complete.")
        return output_path
