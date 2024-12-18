from gdrive.auth import GDriveAuth
from gdrive.utils import count_files_and_folders
from colorama import Fore, Style, init
import logging

# Initialize colorama
init(autoreset=True)

def count_files(source_folder_id: str) -> None:
    """
    Generates a report that shows the total number of files and folders located
    at the root level of the specified source Google Drive folder.

    Args:
        source_folder_id (str): The ID of the Google Drive folder to count files and folders in.
    """
    # Authenticate the Google Drive API and get a service instance
    service = GDriveAuth().get_service()

    # Check if authentication failed, and exit if it did
    if service is None:
        logging.error("Failed to authenticate with Google Drive. Exiting.")
        return
    
    try:
        # Count the number of files and folders at the root of the source folder
        # Unpacks the tuple returned by count_files_and_folders
        file_count, folder_count = count_files_and_folders(service, source_folder_id)
        
        # Only print the report if the counting succeeded
        print(Fore.YELLOW + "\n-----------------------------------------")
        print(Fore.CYAN + f"\n{Fore.GREEN}Total files at the root of the source folder: {Fore.WHITE}{file_count}")
        print(Fore.CYAN + f"\n{Fore.GREEN}Total folders at the root of the source folder: {Fore.WHITE}{folder_count}")
        print(Fore.YELLOW + "\n-----------------------------------------")

    except ValueError as ve:
        # Handle known errors (invalid folder ID)
        print(f"Error: {ve}")
    
    except Exception as e:
        # Handle unknown errors
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
        # Generate the file and folder count report for the source folder
        count_files(source_folder_id)

