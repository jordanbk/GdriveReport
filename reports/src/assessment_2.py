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

        # Query to list all non-trashed files and folders inside the current folder
        query = f"'{folder_id}' in parents and trashed=false"
        response = service.files().list(q=query, fields="files(id, mimeType, name)").execute()

        # Get the list of files and folders
        files = response.get('files', [])

        # Filter out only the subfolders from the list
        subfolders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']

        # Recursively count files and folders inside each subfolder
        for folder in subfolders:
            sub_file_count, sub_folder_count = count_children(folder['id'])
            # Add the counts from the subfolder to the parent folder's totals
            file_count += sub_file_count
            nested_folder_count += sub_folder_count

        return file_count, nested_folder_count

    # Get the total number of files and nested folders for the source folder
    total_files, total_folders = count_children(source_folder_id)
    
    # Output the results
    print(f"Total number of child objects (recursively): {total_files}")
    print(f"Total number of nested folders: {total_folders}")

if __name__ == "__main__":
    """
    Main execution block: Calls the function to generate the report for the specified source folder.
    """
    # Define the source folder ID (hardcoded for this example)
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'  # Replace with your folder ID

    # Generate the recursive count report
    count_recursive(source_folder_id)
