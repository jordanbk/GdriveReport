from typing import Tuple, Optional
from googleapiclient.discovery import Resource
from gdrive.auth import authenticate_gdrive
from gdrive.utils import count_files_and_folders
from colorama import Fore, Style, init

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
    service: Optional[Resource] = authenticate_gdrive()

    if service is None:
        print("Failed to authenticate with Google Drive. Exiting.")
        return

    def count_children(
        folder_id: str, folder_name: str, level: int = 0
    ) -> Tuple[int, int]:
        """
        Recursively count all files and folders in a given folder, including any nested subfolders.
        Prints a tree structure for visualization.

        Args:
            folder_id (str): The ID of the folder for which files and folders are to be counted.
            folder_name (str): The name of the current folder.
            level (int): Current depth level for printing the tree structure.

        Returns:
            tuple: A tuple containing two elements:
                - file_count (int): Total number of files in the folder and its subfolders.
                - nested_folder_count (int): Total number of folders (including subfolders) within the folder.
        """
        # Get the initial file and folder counts for the current folder
        file_count, folder_count = count_files_and_folders(service, folder_id)

        # Print the current folder (with indentation based on the level)
        print(
            "    " * level
            + f"📂 {folder_name} (ID: {folder_id}, Folders: {folder_count}, Files: {file_count})"
        )

        # Track the total number of nested folders
        nested_folder_count = folder_count

        # Query to list all non-trashed files and folders inside the current folder
        query = f"'{folder_id}' in parents and trashed=false"
        response = (
            service.files().list(q=query, fields="files(id, mimeType, name)").execute()
        )

        # Get the list of files and folders
        files = response.get("files", [])

        # Filter out subfolders and files
        subfolders = [
            f for f in files if f["mimeType"] == "application/vnd.google-apps.folder"
        ]
        files = [
            f for f in files if f["mimeType"] != "application/vnd.google-apps.folder"
        ]

        # Print files with indentation based on the level
        for file in files:
            print("    " * (level + 1) + f"📄 {file['name']} (ID: {file['id']})")

        # Recursively count files and folders inside each subfolder
        for folder in subfolders:
            sub_file_count, sub_folder_count = count_children(
                folder["id"], folder["name"], level + 1
            )
            file_count += sub_file_count
            nested_folder_count += sub_folder_count

        return file_count, nested_folder_count

    # Get the total number of files and nested folders for the source folder
    response = service.files().get(fileId=source_folder_id, fields="name").execute()
    root_folder_name = response.get(
        "name", "Root Folder"
    )  # Fallback to "Root Folder" if name not found
    total_files, total_folders = count_children(source_folder_id, root_folder_name)

    # Output the results
    print(Fore.YELLOW + "\n-----------------------------------------")
    print(f"\n{Fore.GREEN}Total number of child objects (recursively) across all top-level folders: {Fore.WHITE}{total_files}")
    print(f"\n{Fore.GREEN}Total number of nested folders within the source folder: {Fore.WHITE}{total_folders}")
    print(f"\n{Fore.GREEN}Total items (files + folders, excluding root folder): {Fore.WHITE}{total_files + total_folders}")
    print(Fore.YELLOW + "\n-----------------------------------------")


if __name__ == "__main__":
    """
    Main execution block: Calls the function to generate the report for the specified source folder.
    """
    # Define the source folder ID (hardcoded for this example)
    source_folder_id = (
        "1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK"  # Replace with your foldear ID
    )

    # Generate the recursive count report
    count_recursive(source_folder_id)
