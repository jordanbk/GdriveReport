from googleapiclient.discovery import Resource
from typing import Tuple, List, Dict, Any
from tqdm import tqdm
from time import sleep
from colorama import Fore, Style

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
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id, mimeType)").execute()
    files = response.get("files", [])

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
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id, mimeType)").execute()

    total_items = 0
    files = response.get("files", [])

    for file in files:
        total_items += 1
        if file["mimeType"] == "application/vnd.google-apps.folder":
            total_items += count_total_items(
                service, file["id"]
            )  # Recursively count subfolder items

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
    query = f"'{folder_id}' in parents and trashed=false"
    response = (
        service.files()
        .list(q=query, fields="files(id, name, mimeType, size, modifiedTime)")
        .execute()
    )
    return response.get("files", [])

# Define a list of colors to cycle through
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def get_rainbow_bar_format(step):
    # Cycle through colors based on the step
    color = colors[step % len(colors)]
    return "{l_bar}%s{bar}%s{r_bar}" % (color, Style.RESET_ALL)

