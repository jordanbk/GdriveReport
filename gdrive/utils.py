from googleapiclient.discovery import Resource
from typing import Tuple, List, Dict, Any
from colorama import Fore, Style
import time
import random

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
    response = service.files().list(q=query, fields=fields).execute()
    return response.get("files", [])



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

    Args:
        service (Resource): The authenticated Google Drive API service.
        folder_id (str): The ID of the folder to count items in.

    Returns:
        int: The total number of items (files and folders) in the folder and its subfolders.
    """
    files = list_drive_files(service, folder_id, "files(id, mimeType)")
    total_items = 0
    
    for file in files:
        total_items += 1
        if file["mimeType"] == "application/vnd.google-apps.folder":
            total_items += count_total_items(service, file["id"])  # Recursively count subfolder items

    return total_items


def get_folder_contents(service: Resource, folder_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve all non-trashed files and folders in a folder, including subfolders.

    Args:
        service (Resource): The Google Drive API service instance.
        folder_id (str): The ID of the folder to retrieve contents from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing file metadata (id, name, mimeType).
    """
    return list_drive_files(service, folder_id, "files(id, name, mimeType, size, modifiedTime)")

def exponential_backoff_retry(api_call, *args, retries=5, **kwargs):
    """
    Attempts to execute an API call with exponential backoff retries in case of timeouts or errors.

    Args:
        api_call (function): The API call function to execute.
        retries (int): Maximum number of retries for the request.
        *args: Arguments to pass to the API call.
        **kwargs: Keyword arguments to pass to the API call.

    Returns:
        result: The result of the API call if successful.
    """
    attempt = 0
    while attempt < retries:
        try:
            # Try executing the API call with both positional and keyword arguments
            return api_call(*args, **kwargs)
        except Exception as e:
            # Print the error and retry after waiting
            print(f"Error executing API call: {e}. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt + random.uniform(0, 1))  # Exponential backoff with jitter
            attempt += 1
    
    # If all retries fail, raise an error
    raise Exception(f"Failed to execute API call after {retries} attempts")


# Define a list of colors to cycle through
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def get_rainbow_bar_format(step):
    # Cycle through colors based on the step
    color = colors[step % len(colors)]
    return "{l_bar}%s{bar}%s{r_bar}" % (color, Style.RESET_ALL)

# https://patorjk.com/software/taag/#p=display&c=bash&f=Slant&t=GdriveReport
def print_welcome():
    welcome_art = r"""
#     ______    __     _            ____                        __ 
#    / ____/___/ /____(_)   _____  / __ \___  ____  ____  _____/ /_
#   / / __/ __  / ___/ / | / / _ \/ /_/ / _ \/ __ \/ __ \/ ___/ __/
#  / /_/ / /_/ / /  / /| |/ /  __/ _, _/  __/ /_/ / /_/ / /  / /_  
#  \____/\__,_/_/  /_/ |___/\___/_/ |_|\___/ .___/\____/_/   \__/  
#                                         /_/                                                                    
"""
    print(welcome_art)

if __name__ == "__main__":
    print_welcome()

