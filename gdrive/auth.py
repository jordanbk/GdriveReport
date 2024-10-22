import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)

# The scope we require for accessing Google Drive metadata
SCOPES = ["https://www.googleapis.com/auth/drive"]


def authenticate_gdrive() -> Optional[Resource]:
    """
    Authenticates the user to the Google Drive API using OAuth 2.0, returning a service instance
    that can be used to interact with the Google Drive API.

    The function checks for previously stored credentials in 'token.json'. If valid credentials
    exist, they are used. If not, the user is prompted to authenticate via a browser, and the
    new credentials are saved for future use.

    Returns:
        Optional[Resource]: A service instance to interact with the Google Drive API, or None if an error occurs.
    """
    # Initialize creds to None. This will hold the credentials if they are available.
    creds: Optional[Credentials] = None
    # Path to the credentials token file, which stores the OAuth 2.0 tokens for Google API access.
    token_file = "token.json"

    try:
        # Step 1: Check if the 'token.json' file exists. This file stores credentials from previous sessions.
        # If it exists, load the credentials from the file.
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            logging.info("Loaded credentials from token.json")
    except HttpError as error:
        logging.error(f"An error occurred while loading token file: {error}")
        return None

    # Step 2: If no valid credentials are found or they are expired, refresh them or start a new login flow.
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # If there's no valid credentials or refresh token, start the OAuth 2.0 login flow.
                # This opens a local web server for the user to authenticate via their browser.
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

            # Step 3: Save the new credentials to 'token.json' so they can be reused in future sessions.
            with open(token_file, "w") as token:
                token.write(creds.to_json())

        except (HttpError, Exception) as error:
            logging.error(f"An error occurred during the OAuth flow or saving credentials: {error}")
            return None

    try:
        # Step 4: Use the credentials to build a Google Drive service object. This service object is used to
        # interact with the Google Drive API.
        service: Resource = build("drive", "v3", credentials=creds)
        logging.info("Successfully authenticated and connected to Google Drive API.")
        return service
    except (HttpError, Exception) as error:
        logging.error(f"An error occurred while connecting to the Google Drive API: {error}")
        return None
