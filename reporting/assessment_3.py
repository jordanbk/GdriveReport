from auth import authenticate_gdrive

def count_total_items(service, folder_id):
    """
    Recursively count all files and subfolders in a Google Drive folder.
    
    Args:
        service: The authenticated Google Drive API service.
        folder_id: The ID of the folder to count items in.
    
    Returns:
        The total number of items (files and folders) in the folder and its subfolders.
    """
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id, mimeType)").execute()
    
    total_items = 0
    files = response.get('files', [])
    
    for file in files:
        total_items += 1
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            total_items += count_total_items(service, file['id'])  # Recursively count subfolder items
    
    return total_items

def copy_folder_contents(source_folder_id, destination_folder_id):
    """
    Copies all contents (files and subfolders) from the source Google Drive folder 
    to the destination folder. This is done recursively for nested folders.
    
    Args:
        source_folder_id (str): The ID of the source Google Drive folder.
        destination_folder_id (str): The ID of the destination Google Drive folder.
    """
    # Authenticate and get access to the Google Drive API
    service = authenticate_gdrive()

    # Step 1: Count total items to copy
    print("Counting total items to copy...")
    total_items = count_total_items(service, source_folder_id)
    print(f"Total items to copy: {total_items}")

    # Initialize total count for progress tracking
    total_items_copied = 0

    def copy_files_and_folders(source_id, dest_id):
        """
        Recursively copy all files and folders from the source folder to the destination folder,
        providing progress feedback to the user.
        
        Args:
            source_id (str): The ID of the current folder being copied.
            dest_id (str): The ID of the destination folder where contents will be copied.
        """
        nonlocal total_items_copied

        # Build the query to get all non-trashed files and folders in the source folder
        query = f"'{source_id}' in parents and trashed=false"
        response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        
        # Retrieve the list of files (and folders) from the API response
        files = response.get('files', [])
        
        # Loop through each file and folder found in the source folder
        for file in files:
            copied_file = None

            # If the current file is a folder, recursively copy its contents
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                folder_metadata = {
                    'name': file['name'],
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [dest_id]
                }
                copied_file = service.files().create(body=folder_metadata, fields='id').execute()
                # print(f"Folder copied: {file['name']}")
                # Recursively copy subfolder
                copy_files_and_folders(file['id'], copied_file['id'])
            else:
                # If the file is not a folder, copy it to the destination
                file_metadata = {
                    'name': file['name'],
                    'parents': [dest_id]
                }
                copied_file = service.files().copy(fileId=file['id'], body=file_metadata).execute()
                # print(f"File copied: {file['name']}")

            # Increment the progress counter and display progress
            total_items_copied += 1
            print(f"Progress: {total_items_copied}/{total_items} items copied.")

    # Start copying the contents of the source folder to the destination
    print(f"Starting to copy contents from {source_folder_id} to {destination_folder_id}...")
    copy_files_and_folders(source_folder_id, destination_folder_id)
    
    # Notify the user that the process has completed
    print(f"Congrats! {total_items_copied} items have been copied from {source_folder_id} to {destination_folder_id}.")

    print(f"Running test to ensure source folder: {source_folder_id} equals destination folder: {destination_folder_id}...")

    # After copying, compare the two folders to check if they are identical
    if compare_folders(service, source_folder_id, destination_folder_id):
        print("The folders are identical after copying.")
    else:
        print("The folders are not identical after copying.")

def compare_folders(service, folder_id1, folder_id2):
    """
    Compare two folders in Google Drive to check if they have the same files and folders.
    
    Args:
        service: The authenticated Google Drive API service.
        folder_id1: The ID of the first folder to compare.
        folder_id2: The ID of the second folder to compare.
    
    Returns:
        True if the folders are equal, False otherwise.
    """
    
    # Retrieve contents of both folders
    folder1_contents = get_folder_contents(service, folder_id1)
    folder2_contents = get_folder_contents(service, folder_id2)
    
    # Sort both lists of files by name (to ensure order-independent comparison)
    folder1_contents.sort(key=lambda x: x['name'])
    folder2_contents.sort(key=lambda x: x['name'])
    
    # Compare the number of files/folders in each folder
    if len(folder1_contents) != len(folder2_contents):
        print(f"Folder content mismatch: {len(folder1_contents)} items in folder 1, {len(folder2_contents)} items in folder 2")
        return False
    
    # Compare each file and folder in both lists
    for file1, file2 in zip(folder1_contents, folder2_contents):
        if file1['name'] != file2['name']:
            print(f"Name mismatch: {file1['name']} in folder 1, {file2['name']} in folder 2")
            return False
        if file1['mimeType'] != file2['mimeType']:
            print(f"Type mismatch: {file1['mimeType']} for {file1['name']} in folder 1, {file2['mimeType']} in folder 2")
            return False

        # If they are subfolders, recursively compare their contents
        if file1['mimeType'] == 'application/vnd.google-apps.folder':
            if not compare_folders(service, file1['id'], file2['id']):
                return False


    # If all checks passed, the folders are equal
    return True

def get_folder_contents(service, folder_id):
    """
    Retrieve all non-trashed files and folders in a folder, including subfolders.
    
    Args:
        service: The Google Drive API service instance.
        folder_id: The ID of the folder to retrieve contents from.
    
    Returns:
        A list of dictionaries containing file metadata (id, name, mimeType).
    """
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id, name, mimeType, size, modifiedTime)").execute()
    return response.get('files', [])

if __name__ == "__main__":
    """
    Main execution block: Prompts the user for the destination folder ID and calls
    the function to copy the contents from the source folder to the destination.
    """
    # Define the source folder ID (hardcoded in this case)
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    
    # Prompt the user for the destination folder ID
    destination_folder_id = input("Please enter the destination folder ID (hint: 1TjN_VohuoM0MaIzYp-z16nVDLiVoWWW1): ")
    
    # Call the function to copy folder contents
    copy_folder_contents(source_folder_id, destination_folder_id)
