import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The scope we require for accessing Google Drive metadata
SCOPES = ["https://www.googleapis.com/auth/drive"]

def authenticate_gdrive():
    """
    Authenticates the user to the Google Drive API using OAuth 2.0, returning a service instance
    that can be used to interact with the Google Drive API.

    The function checks for previously stored credentials in 'token.json'. If valid credentials 
    exist, they are used. If not, the user is prompted to authenticate via a browser, and the 
    new credentials are saved for future use.
    
    Returns:
        service (googleapiclient.discovery.Resource): A service instance to interact with Google Drive API.
    
    Raises:
        HttpError: If an error occurs while attempting to authenticate or build the service.
    """
    
    creds = None
    token_file = "token.json"
    
    # Check if the 'token.json' file exists, which contains previously stored credentials
    if os.path.exists(token_file):
        # Load existing credentials from the file
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If credentials are not valid or do not exist, refresh them or prompt for new login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the access token if expired and refresh token is available
            creds.refresh(Request())
        else:
            # No valid credentials exist, prompt the user to log in using OAuth 2.0
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)  # Opens a local server for OAuth flow
        
        # Save the new credentials to 'token.json' for future use
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    try:
        # Build the Google Drive service using the authenticated credentials
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as error:
        # Handle errors that occur while trying to connect to the Google Drive API
        print(f"An error occurred while connecting to the Google Drive API: {error}")
        return None
