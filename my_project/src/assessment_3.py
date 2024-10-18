from auth import authenticate_gdrive
from utils import count_files_and_folders

def count_recursive(source_folder_id):
    """Generate a report that shows the number of child objects (recursively) for each
    top-level folder under the source folder id and a total of nested folders for the
    source folder."""
    service = authenticate_gdrive()

    def count_children(folder_id):
        file_count, folder_count = count_files_and_folders(service, folder_id)

        nested_folder_count = folder_count
        for folder in [f for f in service.files().list(q=f"'{folder_id}' in parents and trashed=false", fields="files(id, mimeType)").execute().get('files', []) if f['mimeType'] == 'application/vnd.google-apps.folder']:
            sub_file_count, sub_folder_count = count_children(folder['id'])
            file_count += sub_file_count
            nested_folder_count += sub_folder_count

        return file_count, nested_folder_count

    total_files, total_folders = count_children(source_folder_id)
    
    print(f"Total number of child objects (recursively): {total_files}")
    print(f"Total number of nested folders: {total_folders}")

if __name__ == "__main__":
    # source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    source_folder_id = '1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK'
    count_recursive(source_folder_id)

# from auth import authenticate_gdrive

# def copy_folder_contents(source_folder_id, destination_folder_id):
#     service = authenticate_gdrive()

#     def copy_files_and_folders(source_id, dest_id):
#         query = f"'{source_id}' in parents and trashed=false"
#         response = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        
#         files = response.get('files', [])
#         for file in files:
#             copied_file = None
#             if file['mimeType'] == 'application/vnd.google-apps.folder':
#                 folder_metadata = {
#                     'name': file['name'],
#                     'mimeType': 'application/vnd.google-apps.folder',
#                     'parents': [dest_id]
#                 }
#                 copied_file = service.files().create(body=folder_metadata, fields='id').execute()
#                 copy_files_and_folders(file['id'], copied_file['id'])
#             else:
#                 file_metadata = {
#                     'name': file['name'],
#                     'parents': [dest_id]
#                 }
#                 copied_file = service.files().copy(fileId=file['id'], body=file_metadata).execute()

#     copy_files_and_folders(source_folder_id, destination_folder_id)
#     print(f"All contents copied from {source_folder_id} to {destination_folder_id}.")

# if __name__ == "__main__":
#     source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
#     destination_folder_id = 'YOUR_DEST_FOLDER_ID'
#     copy_folder_contents(source_folder_id, destination_folder_id)
