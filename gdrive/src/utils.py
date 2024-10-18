from auth import authenticate_gdrive


def count_files_and_folders(service, folder_id):
    """Count files and folders under a given folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    
    files = response.get('files', [])
    
    file_count = sum(1 for file in files if file['mimeType'] != 'application/vnd.google-apps.folder')
    folder_count = sum(1 for file in files if file['mimeType'] == 'application/vnd.google-apps.folder')

    return file_count, folder_count
