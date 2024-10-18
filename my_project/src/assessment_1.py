from auth import authenticate_gdrive
from utils import count_files_and_folders

def count_files(source_folder_id):
    service = authenticate_gdrive()
    file_count, folder_count = count_files_and_folders(service, source_folder_id)
    
    print(f"Total files: {file_count}")
    print(f"Total folders: {folder_count}")

if __name__ == "__main__":
    # source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V' #netflix source folder id
    source_folder_id = '1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK'
    count_files(source_folder_id)


# def count_files_and_folders(source_folder_id):
#     service = authenticate_gdrive()
    
#     query = f"'{source_folder_id}' in parents and trashed=false"
#     response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    
#     files = response.get('files', [])

#     file_count = sum(map(lambda file: file['mimeType'] != 'application/vnd.google-apps.folder', files))

#     folder_count = sum(map(lambda file: file['mimeType'] == 'application/vnd.google-apps.folder', files))
    
#     print(f"Total files: {file_count}")
#     print(f"Total folders: {folder_count}")

# if __name__ == "__main__":
#     # source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V' #netflix source folder id
#     source_folder_id = '1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK'
#     count_files_and_folders(source_folder_id)