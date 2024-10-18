from auth import authenticate_gdrive
from utils import count_files_and_folders

def count_files(source_folder_id):
    """Write a script to generate a report that shows the number of files and folders in total
    at the root of the source folder."""
    service = authenticate_gdrive()
    file_count, folder_count = count_files_and_folders(service, source_folder_id)
    
    print(f"Total files: {file_count}")
    print(f"Total folders: {folder_count}")

if __name__ == "__main__":
    # source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'
    source_folder_id = '1n1bWgY26PZWXJnA3G5qfaD96kCupuUAK' #personal folder id
    count_files(source_folder_id)