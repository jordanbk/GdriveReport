import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from typing import Optional
import logging

class GDriveAuth:
    _instance = None

    def __new__(cls):
        """
        Implementing the singleton pattern to ensure the same instance is used throughout the program.
        """
        if cls._instance is None:
            cls._instance = super(GDriveAuth, cls).__new__(cls)
        return cls._instance

    def __init__(self, token_file: str = "token.json", credentials_file: str = "credentials.json"):
        self.token_file = token_file
        self.credentials_file = credentials_file
        self.creds = None
        self.service = None
        self.scopes = ["https://www.googleapis.com/auth/drive"]
        if not self.service:
            self.authenticate_gdrive()

    def authenticate_gdrive(self) -> Optional[Resource]:
        """
        Authenticates the user to the Google Drive API using OAuth 2.0, ensuring that the credentials
        are loaded, refreshed, and saved if necessary, and builds the Google Drive service object.
        
        Returns:
            Google Drive service object or None if an error occurs.
        """
        try:
            # Load credentials from token file
            if os.path.exists(self.token_file):
                self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
                logging.info("Loaded credentials from token.json")

            # If credentials are invalid or expired, refresh or reauthenticate
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                    logging.info("Refreshed expired credentials.")
                else:
                    # Start OAuth 2.0 flow if no valid credentials exist
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                    self.creds = flow.run_local_server(port=0)
                    logging.info("OAuth flow completed and credentials obtained.")

                # Save the new or refreshed credentials
                with open(self.token_file, "w") as token:
                    token.write(self.creds.to_json())
                    logging.info("New credentials saved to token.json.")

            # Build and return the Google Drive service
            self.service = build("drive", "v3", credentials=self.creds)
            logging.info("Successfully authenticated and connected to Google Drive API.")
            return self.service

        except (HttpError, Exception) as error:
            logging.error(f"An error occurred during authentication: {error}")
            return None

    def ensure_valid_credentials(self):
        """
        Checks if the credentials are valid before making any API call. Refreshes the credentials if needed.
        """
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            with open(self.token_file, "w") as token:
                token.write(self.creds.to_json())
            logging.info("Credentials were automatically refreshed.")
        elif not self.creds or not self.creds.valid:
            logging.error("Credentials are not valid. Re-authentication may be required.")

    def get_service(self) -> Optional[Resource]:
        """
        Returns the authenticated Google Drive service object. Ensures that credentials are valid.
        """
        self.ensure_valid_credentials()
        return self.service
