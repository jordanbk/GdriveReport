import pytest
from unittest.mock import patch, Mock
from reports.assessment_1 import count_files


@patch("reports.assessment_1.authenticate_gdrive")
@patch("reports.assessment_1.count_files_and_folders")
def test_count_files(
    mock_count_files_and_folders,
    mock_authenticate_gdrive,
    capsys: pytest.CaptureFixture[str],
):
    """
    Test the count_files function in assessment_1.py.
    """
    # Mock the authenticated service object
    mock_service = Mock()
    mock_authenticate_gdrive.return_value = mock_service

    # Mock the return value of count_files_and_folders
    mock_count_files_and_folders.return_value = (10, 5)  # 10 files, 5 folders

    # Call the function to test (this would normally print output)
    source_folder_id = "123456"  # Use a mock folder ID for testing purposes
    count_files(source_folder_id)

    # Check that the authenticate_gdrive function was called once
    mock_authenticate_gdrive.assert_called_once()

    # Check that count_files_and_folders was called with the mock service and correct folder ID
    mock_count_files_and_folders.assert_called_once_with(mock_service, source_folder_id)

    # Capture printed output with capsys
    captured = capsys.readouterr()
    assert "Total files: 10" in captured.out
    assert "Total folders: 5" in captured.out
