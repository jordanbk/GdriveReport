from typing import List, Dict, Any, Optional
from googleapiclient.discovery import Resource
from gdrive.auth import authenticate_gdrive
from gdrive.utils import count_total_items, get_folder_contents, list_drive_files, get_rainbow_bar_format
from tqdm import tqdm
from colorama import Fore, Style, init

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
    service: Optional[Resource] = authenticate_gdrive()

    # Check if authentication failed, and exit if it did
    if service is None:
        print("Failed to authenticate with Google Drive. Exiting.")
        return

    # Step 1: Count total items to copy
    print("\nCounting total items to copy...")
    total_items: int = count_total_items(service, source_folder_id)
    print(f"\nTotal items to copy: {total_items}")

    total_items_copied: int = 0

    # Recursive function to copy files and subfolders
    def copy_files_and_folders(source_id: str, dest_id: str) -> None:
        nonlocal total_items_copied

        # Retrieve all files and folders in the current source folder
        files = list_drive_files(service, source_id, "files(id, name, mimeType)")

        # Iterate over each file or folder in the current folder
        for file in files:
            copied_file: Optional[Dict[str, Any]] = None

            # If the current item is a folder, create the folder in the destination
            if file["mimeType"] == "application/vnd.google-apps.folder":
                folder_metadata = {
                    "name": file["name"],
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [dest_id],
                }
                # Create the folder in the destination and store its metadata
                copied_file = (
                    service.files().create(body=folder_metadata, fields="id").execute()
                )
                # Recursively copy the subfolder contents
                copy_files_and_folders(
                    file["id"], copied_file["id"]
                )
            else:
                # If the current item is a file, copy the file to the destination folder
                file_metadata = {"name": file["name"], "parents": [dest_id]}
                copied_file = (
                    service.files()
                    .copy(fileId=file["id"], body=file_metadata)
                    .execute()
                )
            # Increment and update progress
            total_items_copied += 1
            progress_bar.bar_format = get_rainbow_bar_format(total_items_copied)
            progress_bar.update(1) # Update the progress bar by one unit

    # Start copying the contents of the source folder to the destination
    print(
        f"\nStarting to copy contents from {source_folder_id} to {destination_folder_id}..."
    )

    # Initialize the progress bar with the total number of items to copy
    progress_bar = tqdm(total=total_items, desc="Copying items", unit="item", dynamic_ncols=True)

    # Begin the recursive copying process, starting from the source folder
    copy_files_and_folders(source_folder_id, destination_folder_id)

    # Close the progress bar after copying is complete
    progress_bar.close()

    # Notify the user that all items have been successfully copied
    print(Fore.GREEN + 
        f"\nCongrats! {total_items_copied} items have been copied from {source_folder_id} to {destination_folder_id}."
    )

    # Check if the source and destination folders are identical
    print(
        f"\nRunning test to ensure parity..."
    )
    
    # Use the compare_folders function to check if the folders are identical
    if compare_folders(service, source_folder_id, destination_folder_id):
        print("\nThe folders are identical after copying.")
    else:
        print("\nThe folders are not identical after copying.")


def compare_folders(service: Resource, folder_id1: str, folder_id2: str) -> bool:
    """
    Compare two folders in Google Drive to check if they have the same files and folders.

    Args:
        service (Resource): The authenticated Google Drive API service.
        folder_id1 (str): The ID of the first folder to compare.
        folder_id2 (str): The ID of the second folder to compare.

    Returns:
        bool: True if the folders are equal, False otherwise.
    """

     # Retrieve the contents (files and folders) of both folders using the helper function
    folder1_contents = get_folder_contents(service, folder_id1)
    folder2_contents = get_folder_contents(service, folder_id2)

    # Sort the contents of both folders by the file/folder name to ensure they can be compared in order
    folder1_contents.sort(key=lambda x: x["name"])
    folder2_contents.sort(key=lambda x: x["name"])

    # Check if the number of items in both folders is the same; if not, the folders are not equal
    if len(folder1_contents) != len(folder2_contents):
        print(
            f"Folder content mismatch: {len(folder1_contents)} items in folder 1, {len(folder2_contents)} items in folder 2"
        )
        return False
    
    # Iterate through the contents of both folders simultaneously and compare each item
    for file1, file2 in zip(folder1_contents, folder2_contents):
        # Compare file/folder names and MIME types; if they don't match, the folders are not equal
        if file1["name"] != file2["name"] or file1["mimeType"] != file2["mimeType"]:
            print(f"Mismatch: {file1['name']} in folder 1, {file2['name']} in folder 2")
            return False
        
        # If the item is a folder, recursively compare the contents of both folders
        if file1["mimeType"] == "application/vnd.google-apps.folder":
            if not compare_folders(service, file1["id"], file2["id"]):
                return False
            
    # If all checks pass, the folders are considered equal
    return True


if __name__ == "__main__":
    """
    Main execution block: Prompts the user for the destination folder ID and calls
    the function to copy the contents from the source folder to the destination.
    """
    source_folder_id = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"
    destination_folder_id = input("\nPlease enter the destination folder ID: ")

    copy_folder_contents(source_folder_id, destination_folder_id)
