from typing import List, Dict, Any, Optional
from googleapiclient.discovery import Resource
from gdrive.auth import authenticate_gdrive
from gdrive.utils import count_total_items, get_folder_contents


def copy_folder_contents(source_folder_id: str, destination_folder_id: str) -> None:
    """
    Copies all contents (files and subfolders) from the source Google Drive folder
    to the destination folder. This is done recursively for nested folders.

    Args:
        source_folder_id (str): The ID of the source Google Drive folder.
        destination_folder_id (str): The ID of the destination Google Drive folder.
    """
    service: Optional[Resource] = authenticate_gdrive()

    if service is None:
        print("Failed to authenticate with Google Drive. Exiting.")
        return

    # Step 1: Count total items to copy
    print("Counting total items to copy...")
    total_items: int = count_total_items(service, source_folder_id)
    print(f"Total items to copy: {total_items}")

    total_items_copied: int = 0

    def copy_files_and_folders(source_id: str, dest_id: str) -> None:
        nonlocal total_items_copied
        query = f"'{source_id}' in parents and trashed=false"
        response = (
            service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        )

        files = response.get("files", [])

        for file in files:
            copied_file: Optional[Dict[str, Any]] = None

            if file["mimeType"] == "application/vnd.google-apps.folder":
                folder_metadata = {
                    "name": file["name"],
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [dest_id],
                }
                copied_file = (
                    service.files().create(body=folder_metadata, fields="id").execute()
                )
                copy_files_and_folders(
                    file["id"], copied_file["id"]
                )  # Recursively copy subfolders
            else:
                # Copy individual files
                file_metadata = {"name": file["name"], "parents": [dest_id]}
                copied_file = (
                    service.files()
                    .copy(fileId=file["id"], body=file_metadata)
                    .execute()
                )

            total_items_copied += 1
            print(f"Progress: {total_items_copied}/{total_items} items copied.")

    # Start copying the contents of the source folder to the destination
    print(
        f"Starting to copy contents from {source_folder_id} to {destination_folder_id}..."
    )
    copy_files_and_folders(source_folder_id, destination_folder_id)

    # Notify the user that the process has completed
    print(
        f"Congrats! {total_items_copied} items have been copied from {source_folder_id} to {destination_folder_id}."
    )

    # Check if the source and destination folders are identical
    print(
        f"Running test to ensure source folder: {source_folder_id} equals destination folder: {destination_folder_id}..."
    )

    if compare_folders(service, source_folder_id, destination_folder_id):
        print("The folders are identical after copying.")
    else:
        print("The folders are not identical after copying.")


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
    folder1_contents = get_folder_contents(service, folder_id1)
    folder2_contents = get_folder_contents(service, folder_id2)

    folder1_contents.sort(key=lambda x: x["name"])
    folder2_contents.sort(key=lambda x: x["name"])

    if len(folder1_contents) != len(folder2_contents):
        print(
            f"Folder content mismatch: {len(folder1_contents)} items in folder 1, {len(folder2_contents)} items in folder 2"
        )
        return False

    for file1, file2 in zip(folder1_contents, folder2_contents):
        if file1["name"] != file2["name"] or file1["mimeType"] != file2["mimeType"]:
            print(f"Mismatch: {file1['name']} in folder 1, {file2['name']} in folder 2")
            return False

        if file1["mimeType"] == "application/vnd.google-apps.folder":
            if not compare_folders(service, file1["id"], file2["id"]):
                return False

    return True


if __name__ == "__main__":
    """
    Main execution block: Prompts the user for the destination folder ID and calls
    the function to copy the contents from the source folder to the destination.
    """
    source_folder_id = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"
    destination_folder_id = input("Please enter the destination folder ID: ")

    copy_folder_contents(source_folder_id, destination_folder_id)
