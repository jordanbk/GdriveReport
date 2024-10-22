import unittest
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from gdrive.auth import GDriveAuth
import os

class TestAuthenticateGDrive(unittest.TestCase):

    @patch('gdrive.auth.build')  # Mock the build function from googleapiclient.discovery
    @patch('gdrive.auth.Credentials.from_authorized_user_file')  # Mock loading credentials from file
    def test_authenticate_with_existing_token(self, mock_from_authorized_user_file, mock_build):
        """Test if the authentication works when valid credentials already exist."""
        
        # Create a mock credential object
        mock_creds = MagicMock(spec=Credentials)
        mock_creds.valid = True  # Simulate valid credentials
        
        # Mock the return value of from_authorized_user_file to simulate existing token
        mock_from_authorized_user_file.return_value = mock_creds
        
        # Mock the build function to simulate successful service creation
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Call the function under test
        service = GDriveAuth().get_service()
        
        # Assertions
        self.assertEqual(service, mock_service)  # Ensure the service is returned
        mock_from_authorized_user_file.assert_called_once_with('token.json', ['https://www.googleapis.com/auth/drive'])
        mock_build.assert_called_once_with('drive', 'v3', credentials=mock_creds)

    @patch('gdrive.auth.os.path.exists', return_value=False)  # Simulate no token.json file
    @patch('gdrive.auth.InstalledAppFlow.from_client_secrets_file')  # Mock the OAuth flow creation
    @patch('gdrive.auth.build')  # Mock the build function from googleapiclient.discovery
    def test_authenticate_with_new_token(self, mock_build, mock_from_client_secrets_file, mock_os_path_exists):
        """Test the authentication flow when no existing credentials are found, prompting for new login."""
        
        # Create a mock flow and mock credentials
        mock_flow = MagicMock(spec=InstalledAppFlow)
        mock_creds = MagicMock(spec=Credentials)
        
        # Simulate the OAuth flow returning new credentials
        mock_from_client_secrets_file.return_value = mock_flow
        mock_flow.run_local_server.return_value = mock_creds
        
        # Mock creds.to_json() to return a valid JSON string
        mock_creds.to_json.return_value = '{"token": "fake_token"}'
        
        # Mock the build function to simulate successful service creation
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Call the function under test
        service = GDriveAuth().get_service()
        
        # Assertions
        self.assertEqual(service, mock_service)  # Ensure the service is returned
        mock_from_client_secrets_file.assert_called_once_with('credentials.json', ['https://www.googleapis.com/auth/drive'])
        mock_flow.run_local_server.assert_called_once()
        mock_build.assert_called_once_with('drive', 'v3', credentials=mock_creds)


    @patch('googleapiclient.discovery.build')
    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    def test_authentication_failure(self, mock_from_authorized_user_file, mock_build):
        """Test handling of HttpError during authentication."""

        # Create a mock response object with the required attributes
        mock_response = MagicMock()
        mock_response.status = 403
        mock_response.reason = 'Forbidden'

        # Mock an HttpError with a valid response and URI
        mock_from_authorized_user_file.side_effect = HttpError(mock_response, b'some error', uri='http://mock.url')

        # Call the function under test, expecting None as a result due to the error
        service = GDriveAuth().get_service()

        # Assertions
        self.assertIsNone(service)  # Ensure the function returns None due to the HttpError
        mock_from_authorized_user_file.assert_called_once_with('token.json', ['https://www.googleapis.com/auth/drive'])
        mock_build.assert_not_called()  # Ensure build was never called due to the error


if __name__ == '__main__':
    unittest.main()
