from .auth import authenticate_gdrive  
from .assessment_1 import count_files_and_folders  
import sys

def main():
    print("Authenticating Google Drive...")
    service = authenticate_gdrive()

    # Specify the source folder ID here or get it from user input
    source_folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'

    if len(sys.argv) > 1:
        if sys.argv[1] == 'count':
            print("Counting files and folders...")
            count_files_and_folders(source_folder_id)
        else:
            print(f"Unknown command: {sys.argv[1]}")
    else:
        print("No command provided. Use 'count' as a command.")

if __name__ == '__main__':
    main()
