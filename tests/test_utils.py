import pytest
from gdrive.auth import authenticate_gdrive
from gdrive.utils import count_files_and_folders

@pytest.mark.parametrize("folder_id", ["1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK"])
def test_count_files_and_folders(folder_id):
    """Test the count_files_and_folders utility function."""
    
    # Get authenticated service object
    service = authenticate_gdrive()
    
    # Call the function to test
    file_count, folder_count = count_files_and_folders(service, folder_id)
    
    # Assertions
    assert isinstance(file_count, int), "file_count should be an integer"
    assert isinstance(folder_count, int), "folder_count should be an integer"
    assert file_count >= 0, "file_count should not be negative"
    assert folder_count >= 0, "folder_count should not be negative"
