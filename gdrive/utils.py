from googleapiclient.discovery import Resource
from typing import Tuple, Callable, List, Dict, Any
from colorama import Fore, Style
import time
import random
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)

def exponential_backoff_retry(retries: int = 5) -> Callable[..., Any]:
    """
    Decorator that applies exponential backoff retries to a function in case of an error.
    
    The wrapped function will attempt to execute, and if it raises an exception, 
    it will retry after a delay that increases exponentially with each attempt.
    This continues until the function succeeds or the maximum number of retries is reached.
    
    Args:
        retries (int): The maximum number of retry attempts before raising an exception. 
                       Defaults to 5 retries.
    Returns:
        Callable[..., Any]: A wrapped function that includes the retry logic.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            while attempt < retries:
                try:
                    # Try executing the function
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error executing {func.__name__}: {e}. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt + random.uniform(0, 1))  # Exponential backoff with jitter
                    attempt += 1
            raise Exception(f"Failed to execute {func.__name__} after {retries} retries")
        return wrapper
    return decorator

@exponential_backoff_retry()
def execute_with_retry(request):
    """
    Helper function to execute a Google Drive API request with retry logic.
    Applies retries only to the execute() calls to ensure that only the API call itself is retried.
    """
    return request.execute()

def list_drive_files(service: Resource, folder_id: str, fields: str) -> List[Dict[str, Any]]:
    """
    Helper function to query Google Drive API for files and folders in a specific folder.
    
    Args:
        service (Resource): Google Drive API service instance.
        folder_id (str): ID of the folder to query.
        fields (str): Fields to retrieve for each file.
        
    Returns:
        List[Dict[str, Any]]: List of file metadata.
    """
    query = f"'{folder_id}' in parents and trashed=false"
    request = service.files().list(q=query, fields=fields)
    response = execute_with_retry(request)
    return response.get("files", [])

def count_children_recursively(service: Resource, folder_id: str, folder_name: str, level: int = 0) -> Tuple[int, int]:
    """
    Recursively count all files and folders in a given folder, including any nested subfolders.
    Prints a tree structure for visualization.

    Args:
        service (Resource): Google Drive API service instance.
        folder_id (str): The ID of the folder for which files and folders are to be counted.
        folder_name (str): The name of the current folder.
        level (int): Current depth level for printing the tree structure.

    Returns:
        tuple: A tuple containing two elements:
            - file_count (int): Total number of files in the folder and its subfolders.
            - nested_folder_count (int): Total number of folders (including subfolders) within the folder.
    """
    file_count, folder_count = count_files_and_folders(service, folder_id)

    # Print the current folder (with indentation based on the level)
    print("    " * level + f"📂 {folder_name} (ID: {folder_id}, Folders: {folder_count}, Files: {file_count})")

    nested_folder_count = folder_count
    files = list_drive_files(service, folder_id, "files(id, mimeType, name, webViewLink)")

    # Filter out subfolders and files
    subfolders = [f for f in files if f["mimeType"] == "application/vnd.google-apps.folder"]
    files = [f for f in files if f["mimeType"] != "application/vnd.google-apps.folder"]

    # Print files with indentation based on the level
    for file in files:
        file_url = file.get("webViewLink", "No URL available")
        print("    " * (level + 1) + f"📄 {file['name']} (ID: {file['id']}) - \033]8;;{file_url}\033\\webViewLink\033]8;;\033\\")

    # Recursively count files and folders inside each subfolder
    for folder in subfolders:
        sub_file_count, sub_folder_count = count_children_recursively(service, folder["id"], folder["name"], level + 1)
        file_count += sub_file_count
        nested_folder_count += sub_folder_count

    return file_count, nested_folder_count


def count_files_and_folders(service: Resource, folder_id: str) -> Tuple[int, int]:
    """
    Counts the number of files and folders that are direct children of a given Google Drive folder.

    Args:
        service (googleapiclient.discovery.Resource): Authenticated Google Drive API service instance.
        folder_id (str): The ID of the folder for which to count the files and folders.

    Returns:
        tuple: A tuple containing two integers:
            - file_count (int): The number of files in the folder.
            - folder_count (int): The number of folders in the folder.
    """
    files = list_drive_files(service, folder_id, "files(id, mimeType)")
    
    file_count = sum(
        1 for file in files if file["mimeType"] != "application/vnd.google-apps.folder"
    )
    folder_count = sum(
        1 for file in files if file["mimeType"] == "application/vnd.google-apps.folder"
    )
    
    return file_count, folder_count

def count_total_items(service: Resource, folder_id: str) -> int:
    """
    Recursively count all files and subfolders in a Google Drive folder.
    """
    file_count, folder_count = count_files_and_folders(service, folder_id)
    total_items = file_count + folder_count
    subfolders = [file for file in list_drive_files(service, folder_id, 'files(id, mimeType)') if file["mimeType"] == "application/vnd.google-apps.folder"]
    
    for subfolder in subfolders:
        total_items += count_total_items(service, subfolder["id"])  # Recursively count subfolder items
    return total_items

def get_folder_contents(service: Resource, folder_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves all non-trashed files and folders directly located in the specified Google Drive folder.

    Args:
        service (Resource): The Google Drive API service instance.
        folder_id (str): The ID of the folder to retrieve contents from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing file metadata (id, name, mimeType).
    """
    return list_drive_files(service, folder_id, "files(id, name, mimeType, size, modifiedTime)")

def create_folder_with_retry(service: Resource, file: Dict[str, Any], dest_id: str) -> Dict[str, Any]:
    """
    Helper function to create a folder with exponential backoff retry logic.

    Args:
        service (Resource): Google Drive API service instance.
        file (dict): The file/folder metadata.
        dest_id (str): The ID of the destination folder where the new folder will be created.

    Returns:
        dict: Metadata of the created folder.
    """
    folder_metadata = {
        "name": file["name"],
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [dest_id],
    }
    request = service.files().create(body=folder_metadata, fields="id")
    return execute_with_retry(request)

def copy_file_with_retry(service: Resource, file: Dict[str, Any], dest_id: str) -> Dict[str, Any]:
    """
    Helper function to copy a file with exponential backoff retry logic.

    Args:
        service (Resource): Google Drive API service instance.
        file (dict): The file metadata.
        dest_id (str): The ID of the destination folder where the file will be copied.

    Returns:
        dict: Metadata of the copied file.
    """
    file_metadata = {"name": file["name"], "parents": [dest_id]}
    request = service.files().copy(fileId=file["id"], body=file_metadata)
    return execute_with_retry(request)

def are_folders_identical(service: Resource, folder_id1: str, folder_id2: str) -> bool:
    """
    Compare two folders in Google Drive to check if they have the same files and folders,
    excluding size checks for Google-native files (Google Docs, Sheets, Slides).
    
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
        logging.warning(f"Mismatch in item count between folder {folder_id1} and {folder_id2}")
        return False

    # Iterate through the contents of both folders simultaneously and compare each item
    for file1, file2 in zip(folder1_contents, folder2_contents):
        # Compare file/folder names and MIME types; if they don't match, the folders are not equal
        if file1["name"] != file2["name"] or file1["mimeType"] != file2["mimeType"]:
            logging.warning(f"Mismatch: {file1['name']} in folder 1, {file2['name']} in folder 2")
            return False

        # If the item is a file and is not a Google-native file, compare its size
        if file1["mimeType"] != "application/vnd.google-apps.folder":
            if not file1["mimeType"].startswith("application/vnd.google-apps."):  # Exclude Google-native files
                size1 = int(file1.get("size", 0))  # Get the size of file1 (default to 0 if not present)
                size2 = int(file2.get("size", 0))  # Get the size of file2 (default to 0 if not present)
                if size1 != size2:
                    logging.WARNING(
                        f"Size mismatch for file {file1['name']}: "
                        f"{size1} bytes in folder 1, {size2} bytes in folder 2"
                    )
                    return False

        # If the item is a folder, recursively compare the contents of both folders
        if file1["mimeType"] == "application/vnd.google-apps.folder":
            if not are_folders_identical(service, file1["id"], file2["id"]):
                return False

    # If all checks pass, the folders are considered equal
    return True

def get_rainbow_bar_format(step: int) -> str:
    """
    Generates a progress bar format string that changes color based on the step number.
    
    The function cycles through a list of predefined colors (stored in `colors`), and selects 
    a color based on the current step. It formats the progress bar with the selected color 
    and resets the color formatting at the end.

    Args:
        step (int): The current step or iteration number, which determines the color of the progress bar.

    Returns:
        str: A formatted string to be used as the progress bar format with the selected color.
    """
    # Define a list of colors to cycle through
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    # Cycle through colors based on the step
    color = colors[step % len(colors)]
    return f"{'{l_bar}'}{color}{'{bar}'}{Style.RESET_ALL}{'{r_bar}'}"

# https://patorjk.com/software/taag/#p=display&c=bash&f=Slant&t=GdriveReport
def print_welcome() -> None:
    """
    Prints a welcome ASCII art to the console.
    """
    welcome_art = r"""
#     ______    __     _            ____                        __ 
#    / ____/___/ /____(_)   _____  / __ \___  ____  ____  _____/ /_
#   / / __/ __  / ___/ / | / / _ \/ /_/ / _ \/ __ \/ __ \/ ___/ __/
#  / /_/ / /_/ / /  / /| |/ /  __/ _, _/  __/ /_/ / /_/ / /  / /_  
#  \____/\__,_/_/  /_/ |___/\___/_/ |_|\___/ .___/\____/_/   \__/  
#                                         /_/                                                                    
"""
    print(welcome_art)

