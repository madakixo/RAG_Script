import os
import io
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveLoader:
    def __init__(self, credentials_info=None, credentials_path='credentials.json'):
        """
        Initializes the DriveLoader with a Service Account.
        credentials_info: A dictionary containing service account info.
        credentials_path: Path to the service account JSON file.
        """
        self.creds = None
        self.service = None
        
        if credentials_info:
            self.creds = service_account.Credentials.from_service_account_info(
                credentials_info, scopes=SCOPES)
        elif os.path.exists(credentials_path):
            self.creds = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=SCOPES)
        else:
            # Try to get from environment variable if neither provided
            env_creds = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
            if env_creds:
                try:
                    info = json.loads(env_creds)
                    self.creds = service_account.Credentials.from_service_account_info(
                        info, scopes=SCOPES)
                except Exception as e:
                    raise ValueError(f"Error parsing GOOGLE_SERVICE_ACCOUNT_JSON: {e}")
            else:
                raise FileNotFoundError("Service account credentials not found. Provide credentials_info, credentials.json, or set GOOGLE_SERVICE_ACCOUNT_JSON.")

        self.service = build('drive', 'v3', credentials=self.creds)

    def download_file(self, file_id, output_path):
        """Downloads a file from Google Drive."""
        try:
            request = self.service.files().get_media(fileId=file_id)

            fh = io.FileIO(output_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            print(f"Downloading file ID: {file_id} to {output_path}...")
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download {int(status.progress() * 100)}%.")
            print("Download complete.")
            return output_path
        except Exception as e:
            print(f"Error downloading from Drive: {e}")
            raise e
