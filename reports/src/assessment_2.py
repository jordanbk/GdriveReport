from auth import authenticate_gdrive
from utils import count_files_and_folders

def count_recursive(source_folder_id):
    """
    Generates a report that recursively counts the total number of child objects (files and folders)
    for each top-level folder inside the given source folder. It also calculates the total number of
    nested folders within the source folder.

    Args:
        source_folder_id (str): The ID of the source Google Drive folder.
    """
    # Authenticate and get access to the Google Drive API
    service = authenticate_gdrive()

    def count_children(folder_id):
        """
        Recursively count all files and folders in a given folder, including any nested subfolders.
        
        Args:
            folder_id (str): The ID of the folder for which files and folders are to be counted.

        Returns:
            tuple: A tuple containing two elements:
                - file_count (int): Total number of files in the folder and its subfolders.
                - nested_folder_count (int): Total number of folders (including subfolders) within the folder.
        """
        # Get the initial file and folder counts for the current folder
        file_count, folder_count = count_files_and_folders(service, folder_id)
        
        # Track the total number of nested folders
        nested_folder_count = folder_count

        # Query to list all non-trashed
