from gdrive.auth import authenticate_gdrive
from gdrive.utils import count_files_and_folders
from googleapiclient.discovery import Resource
from colorama import Fore, Style, init

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
    service: Resource = authenticate_gdrive()

    # Check if authentication failed, and exit if it did
    if service is None:
        print("Failed to authenticate with Google Drive. Exiting.")
        return

    # Count the number of files and folders at the root of the source folder
    file_count, folder_count = count_files_and_folders(service, source_folder_id)

    # Output the total number of files and folders at the root level
    print(Fore.YELLOW + "\n-----------------------------------------")
    print(
        Fore.CYAN
        + f"\n{Fore.GREEN}Total files at the root of the source folder: {Fore.WHITE}{file_count}"
    )
    print(
        Fore.CYAN
        + f"\n{Fore.GREEN}Total folders at the root of the source folder: {Fore.WHITE}{folder_count}"
    )
    print(Fore.YELLOW + "\n-----------------------------------------")


if __name__ == "__main__":
    """
    Main execution block: Calls the function to generate the report for the specified source folder.
    """
    # Define the source folder ID (hardcoded for this example)
    source_folder_id: str = (
        "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"  # Replace with your folder ID
    )

    # Generate the file and folder count report for the source folder
    count_files(source_folder_id)
