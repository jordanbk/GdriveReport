from auth import authenticate_gdrive

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

    def copy_files_and_folders(source_id, dest_id):
        """
        Recursively copy all files and folders from the source folder to the destination folder.
        
        Args:
            source_id (str): The ID of the current folder being copied.
            dest_id (str): The ID of the destination folder where contents will be copied.
        """
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
                # Metadata for the folder to be created in the destination
                folder_metadata = {
                    'name': file['name'],  # Keep the folder name the same
                    'mimeType': 'application/vnd.google-apps.folder',  # Type as folder
                    'parents': [dest_id]  # Set the destination folder as its parent
                }
                # Create the folder in the destination
                copied_file = service.files().create(body=folder_metadata, fields='id').execute()
                # Recursively copy the contents of this subfolder
                copy_files_and_folders(file['id'], copied_file['id'])
            else:
                # If the file is not a folder, copy it to the destination
                file_metadata = {
                    'name': file['name'],  # Keep the file name the same
                    'parents': [dest_id]  # Set the destination folder as its parent
                }
                # Copy the file to the destination folder
                copied_file = service.files().copy(fileId=file['id'], body=file_metadata).execute()

    # Start copying the contents of the source folder to the destination
    copy_files_and_folders(source_folder_id, destination_folder_id)
    
    # Notify the user that the process has completed
    print(f"Congrats! All contents have been copied from {source_folder_id} to {destination_folder_id}.")

if __name__ == "__main__":
    """
    Main execution block: Prompts the user for the destination folder ID and calls
    the function to copy the contents from the source folder to the destination.
    """
    # Define the source folder ID (hardcoded in this case)
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    
    # Prompt the user for the destination folder ID
    destination_folder_id = input("Please enter the destination folder ID (hint:1TjN_VohuoM0MaIzYp-z16nVDLiVoWWW1): ")
    
    # Call the function to copy folder contents
    copy_folder_contents(source_folder_id, destination_folder_id)
