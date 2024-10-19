from gdrive.auth import authenticate_gdrive
from gdrive.utils import count_files_and_folders


def count_files(source_folder_id):
    """
    Generates a report that shows the total number of files and folders located
    at the root level of the specified source Google Drive folder.

    Args:
        source_folder_id (str): The ID of the Google Drive folder to count files and folders in.
    """
    # Authenticate and get access to the Google Drive API
    service = authenticate_gdrive()

    # Count the number of files and folders at the root of the source folder
    file_count, folder_count = count_files_and_folders(service, source_folder_id)

    # Output the total number of files and folders at the root level
    print(f"Total files: {file_count}")
    print(f"Total folders: {folder_count}")


if __name__ == "__main__":
    """
    Main execution block: Calls the function to generate the report for the specified source folder.
    """
    # Define the source folder ID (hardcoded for this example)
    source_folder_id = (
        "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"  # Replace with your folder ID
    )

    # Generate the file and folder count report for the source folder
    count_files(source_folder_id)
