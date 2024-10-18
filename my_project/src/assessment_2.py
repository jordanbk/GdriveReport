from auth import authenticate_gdrive
from utils import count_files_and_folders

def count_recursive(source_folder_id):
    """Generate a report that shows the number of child objects (recursively) for each
    top-level folder under the source folder id and a total of nested folders for the
    source folder."""
    service = authenticate_gdrive()

    def count_children(folder_id):
        """Count all the files and folders inside the subfolder.
        Recursively call itself for any nested subfolders inside that subfolder."""
        # Get the initial file and folder counts for the current folder
        file_count, folder_count = count_files_and_folders(service, folder_id)

        nested_folder_count = folder_count
        
        # List all files and folders inside the current folder
        query = f"'{folder_id}' in parents and trashed=false"
        response = service.files().list(q=query, fields="files(id, mimeType, name)").execute()
        files = response.get('files', [])

        # Filter out folders from the list
        subfolders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
        
        # Recursively count the files and folders inside each subfolder
        for folder in subfolders:
            sub_file_count, sub_folder_count = count_children(folder['id'])
            file_count += sub_file_count
            nested_folder_count += sub_folder_count

        return file_count, nested_folder_count

    total_files, total_folders = count_children(source_folder_id)
    
    print(f"Total number of child objects (recursively): {total_files}")
    print(f"Total number of nested folders: {total_folders}")

if __name__ == "__main__":
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    # source_folder_id = '1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK'
    count_recursive(source_folder_id)
