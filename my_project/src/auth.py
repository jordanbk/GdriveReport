import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def authenticate_gdrive():
    """Authenticates the user to Google Drive API and returns a service instance."""
    creds = None
    token_file = "token.json"
    
    # Load credentials from token.json if available
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # Refresh credentials or prompt login if invalid or expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "my_project/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save new credentials for future use
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred while connecting to the Google Drive API: {error}")
        return None
