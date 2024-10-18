from auth import authenticate_gdrive

def copy_folder_contents(source_folder_id, destination_folder_id):
    service = authenticate_gdrive()

    def copy_files_and_folders(source_id, dest_id):
        query = f"'{source_id}' in parents and trashed=false"
        response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        
        files = response.get('files', [])
        for file in files:
            copied_file = None
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                folder_metadata = {
                    'name': file['name'],
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [dest_id]
                }
                copied_file = service.files().create(body=folder_metadata, fields='id').execute()
                copy_files_and_folders(file['id'], copied_file['id'])
            else:
                file_metadata = {
                    'name': file['name'],
                    'parents': [dest_id]
                }
                copied_file = service.files().copy(fileId=file['id'], body=file_metadata).execute()

    copy_files_and_folders(source_folder_id, destination_folder_id)
    print(f"All contents copied from {source_folder_id} to {destination_folder_id}.")

if __name__ == "__main__":
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    destination_folder_id = 'YOUR_DEST_FOLDER_ID'
    copy_folder_contents(source_folder_id, destination_folder_id)
