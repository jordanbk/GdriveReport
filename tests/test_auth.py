import pytest
from gdrive.auth import authenticate_gdrive


def test_authenticate_gdrive():
    """Test if authenticate_gdrive returns a valid service object."""
    service = authenticate_gdrive()

    assert service is not None, "The Google Drive service should not be None"
    assert hasattr(
        service, "files"
    ), "The service object should have a 'files' attribute"
