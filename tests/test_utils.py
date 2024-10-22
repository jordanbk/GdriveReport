import unittest
from unittest.mock import patch, MagicMock
from gdrive.utils import list_drive_files, count_files_and_folders, count_children_recursively, are_folders_identical

class TestUtils(unittest.TestCase):

    # Called before every test method
    def setUp(self):
        self.service = MagicMock()  # A mock Google Drive service

    # Called after every test method
    def tearDown(self):
        pass

    def test_list_drive_files_with_retry(self):
        mock_files = {
            'files': [
                {'id': '1', 'name': 'file1.txt', 'mimeType': 'text/plain'},
                {'id': '2', 'name': 'folder1', 'mimeType': 'application/vnd.google-apps.folder'},
            ]
        }

        # First call raises an exception, second call succeeds
        self.service.files().list().execute.side_effect = [Exception("Temporary error"), mock_files]

        # Call the function
        folder_id = '123456'
        fields = 'files(id, name, mimeType)'
        files = list_drive_files(self.service, folder_id, fields)

        # Assertions
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0]['name'], 'file1.txt')
        self.assertEqual(self.service.files().list.call_count, 2)  # Should be called twice due to retry

    @patch('gdrive.utils.list_drive_files')  # Mock the list_drive_files function
    def test_count_files_and_folders(self, mock_list_drive_files):
        # Setup the mock to return a fake list of files and folders
        mock_files = [
            {'id': '1', 'mimeType': 'text/plain'},
            {'id': '2', 'mimeType': 'application/vnd.google-apps.folder'},
        ]
        mock_list_drive_files.return_value = mock_files

        # Call the function with the mocked service
        folder_id = '123456'
        file_count, folder_count = count_files_and_folders(self.service, folder_id)

        # Assertions
        mock_list_drive_files.assert_called_once_with(self.service, folder_id, 'files(id, mimeType)')
        self.assertEqual(file_count, 1)
        self.assertEqual(folder_count, 1)

    @patch('gdrive.utils.list_drive_files')  # Mock the list_drive_files function
    @patch('builtins.print')  # Mock print to suppress output in the test
    def test_count_children_recursively(self, mock_print, mock_list_drive_files):
        # Mock response for first call and for recursive call to prevent infinite recursion
        mock_list_drive_files.side_effect = [
            [
                {'id': '1', 'mimeType': 'text/plain', 'name': 'file1.txt'},
                {'id': '2', 'mimeType': 'application/vnd.google-apps.folder', 'name': 'folder1'},
            ],
            []  # Empty list for recursive call to prevent further recursion
        ]

        # Call the function with the mocked service
        folder_id = '123456'
        folder_name = 'test_folder_name'
        file_count, nested_folder_count = count_children_recursively(self.service, folder_id, folder_name)

        # Assertions
        self.assertEqual(file_count, 1)
        self.assertEqual(nested_folder_count, 1)

    @patch('gdrive.utils.get_folder_contents')  # Mock the get_folder_contents function
    def test_are_folders_identical(self, mock_get_folder_contents):
        # Mock folder contents for two folders
        folder1_contents = [{'id': '1', 'name': 'file1.txt', 'mimeType': 'text/plain', 'size': 100}]
        folder2_contents = [{'id': '1', 'name': 'file1.txt', 'mimeType': 'text/plain', 'size': 100}]
        mock_get_folder_contents.side_effect = [folder1_contents, folder2_contents]

        # Call the function with the mocked service
        folder_id1 = '123456'
        folder_id2 = '789101'
        result = are_folders_identical(self.service, folder_id1, folder_id2)

        # Assertions
        self.assertTrue(result)
        mock_get_folder_contents.assert_any_call(self.service, folder_id1)
        mock_get_folder_contents.assert_any_call(self.service, folder_id2)

if __name__ == '__main__':
    unittest.main()
