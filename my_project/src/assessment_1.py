from auth import authenticate_gdrive

def count_files_and_folders(source_folder_id):
    service = authenticate_gdrive()
    
    query = f"'{source_folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    
    files = response.get('files', [])
    file_count = sum(1 for file in files if file['mimeType'] != 'application/vnd.google-apps.folder')
    folder_count = sum(1 for file in files if file['mimeType'] == 'application/vnd.google-apps.folder')
    
    print(f"Total files: {file_count}")
    print(f"Total folders: {folder_count}")

if __name__ == "__main__":
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    count_files_and_folders(source_folder_id)
