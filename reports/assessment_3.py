from typing import Dict, Any, Optional
from gdrive.auth import GDriveAuth
from gdrive.utils import (
    count_total_items,
    list_drive_files,
    are_folders_identical,
    get_rainbow_bar_format,
    create_folder_with_retry,
    copy_file_with_retry
)
from tqdm import tqdm
from colorama import Fore, init
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Initialize colorama
init(autoreset=True)

def copy_folder_contents(source_folder_id: str, destination_folder_id: str) -> None:
    """
    Copies all contents (files and subfolders) from the source Google Drive folder
    to the destination folder. This is done recursively for nested folders.

    Args:
        source_folder_id (str): The ID of the source Google Drive folder.
        destination_folder_id (str): The ID of the destination Google Drive folder.
    """

    # Authenticate the Google Drive API and get a service instance
    service = GDriveAuth().get_service()

    # Check if authentication failed, and exit if it did
    if service is None:
        logging.error("Failed to authenticate with Google Drive. Exiting.")
        return

    # Step 1: Count total items to copy
    print("\nCounting total items to copy...")
    total_items: int = count_total_items(service, source_folder_id)
    print(f"\nTotal items to copy: {total_items}")

    total_items_copied: int = 0

    # Recursive function to copy files and subfolders
    def recursively_copy_contents(source_id: str, dest_id: str) -> None:
        nonlocal total_items_copied

        # Retrieve all files and folders in the current source folder
        files = list_drive_files(service, source_id, "files(id, name, mimeType)")

        # Iterate over each file or folder in the current folder
        for file in files:
            copied_file: Optional[Dict[str, Any]] = None

            # If the current item is a folder, create the folder in the destination
            if file["mimeType"] == "application/vnd.google-apps.folder":
                copied_file = create_folder_with_retry(service, file, dest_id)

                # Recursively copy the subfolder contents
                recursively_copy_contents(file["id"], copied_file["id"])
            else:
                # If the current item is a file, copy the file to the destination folder
                copy_file_with_retry(service, file, dest_id)

            # Increment and update progress
            total_items_copied += 1
            progress_bar.bar_format = get_rainbow_bar_format(total_items_copied)
            progress_bar.update(1)  # Update the progress bar by one unit

    # Start copying the contents of the source folder to the destination
    print(f"\nStarting to copy contents from {source_folder_id} to {destination_folder_id}...")

    # Initialize the progress bar with the total number of items to copy
    progress_bar = tqdm(total=total_items, desc="Copying items", unit="item", dynamic_ncols=True)

    # Begin the recursive copying process, starting from the source folder
    recursively_copy_contents(source_folder_id, destination_folder_id)

    # Close the progress bar after copying is complete
    progress_bar.close()

    # Notify the user that all items have been successfully copied
    print(Fore.GREEN + f"\nCongrats! {total_items_copied} items have been copied from {source_folder_id} to {destination_folder_id}.")

    # Check if the source and destination folders are identical
    print(f"\nRunning test to ensure parity...")

    # Use function to check if the folders are identical
    if are_folders_identical(service, source_folder_id, destination_folder_id):
        print("\nThe folders are identical after copying.")
    else:
        print("\nThe folders are not identical after copying.")

if __name__ == "__main__":
    """
    Main execution block: Prompts the user for the destination folder ID and calls
    the function to copy the contents from the source folder to the destination.
    """
    source_folder_id: str = input("Please enter the source folder ID: ").strip()
    destination_folder_id: str = input("\nPlease enter the destination folder ID: ").strip()

    if not source_folder_id or not destination_folder_id:
        logging.error("Source and/or destination folder ID is missing. Exiting.")
    else:
        copy_folder_contents(source_folder_id, destination_folder_id)
