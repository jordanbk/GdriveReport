from gdrive.auth import GDriveAuth
from gdrive.utils import count_children_recursively
from googleapiclient.errors import HttpError
from colorama import Fore, init
import logging

# Initialize colorama
init(autoreset=True)

def count_recursive(source_folder_id: str) -> None:
    """
    Generates a report that recursively counts the total number of child objects (files and folders)
    for each top-level folder inside the given source folder. It also prints a tree structure showing
    the hierarchy of subfolders and files, including folder names and IDs.

    Args:
        source_folder_id (str): The ID of the source Google Drive folder.
    """
    # Authenticate the Google Drive API and get a service instance
    service = GDriveAuth().get_service()

    # Check if authentication failed, and exit if it did
    if service is None:
        logging.error("Failed to authenticate with Google Drive. Exiting.")
        return

    try:
        # Get the name of the root folder using the Google Drive API
        response = service.files().get(fileId=source_folder_id, fields="name").execute()
        root_folder_name = response.get("name", "Root Folder")  # Fallback to "Root Folder" if name not found

        # Start the recursive counting for the source folder
        total_files, total_folders = count_children_recursively(service, source_folder_id, root_folder_name)

        # Output the results if counting succeeded
        print(Fore.YELLOW + "\n-----------------------------------------")
        print(f"\n{Fore.GREEN}Total number of child objects (recursively) across all top-level folders: {Fore.WHITE}{total_files}")
        print(f"\n{Fore.GREEN}Total number of nested folders within the source folder: {Fore.WHITE}{total_folders}")
        print(f"\n{Fore.GREEN}Total items (files + folders, excluding root folder): {Fore.WHITE}{total_files + total_folders}")
        print(Fore.YELLOW + "\n-----------------------------------------")

    except HttpError as he:
        # Handle HTTP-related errors (e.g., invalid folder ID or permissions issues)
        logging.error(f"An HTTP error occurred: {he}")
        print(f"Error: Unable to access folder {source_folder_id}. Please check the folder ID and your permissions.")
    
    except Exception as e:
        # Handle general errors
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    """
    Main execution block: Calls the function to generate the report for the specified source folder.
    """
    # Prompt for user input
    source_folder_id: str = input("Please enter the Google Drive folder ID: ").strip()

    if not source_folder_id:
        logging.error("No folder ID provided. Exiting.")
    else:
        # Generate the recursive count report
        count_recursive(source_folder_id)
