def count_files_and_folders(service, folder_id):
    """
    Counts the number of files and folders that are direct children of a given Google Drive folder.

    This function queries the Google Drive API for all non-trashed items (both files and folders)
    under the specified folder and then counts how many are files and how many are folders.

    Args:
        service (googleapiclient.discovery.Resource): Authenticated Google Drive API service instance.
        folder_id (str): The ID of the folder for which to count the files and folders.

    Returns:
        tuple: A tuple containing two integers:
            - file_count (int): The number of files in the folder.
            - folder_count (int): The number of folders in the folder.
    """

    # Query to list all non-trashed files and folders directly inside the given folder
    query = f"'{folder_id}' in parents and trashed=false"

    # Execute the query to get the list of files and folders
    response = (
        service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    )

    # Retrieve the list of files and folders from the response
    files = response.get("files", [])

    # Count the number of files (items that are not folders)
    file_count = sum(
        1 for file in files if file["mimeType"] != "application/vnd.google-apps.folder"
    )

    # Count the number of folders
    folder_count = sum(
        1 for file in files if file["mimeType"] == "application/vnd.google-apps.folder"
    )

    # Return the counts as a tuple: (number of files, number of folders)
    return file_count, folder_count
