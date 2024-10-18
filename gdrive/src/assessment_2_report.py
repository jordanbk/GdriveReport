import time
from auth import authenticate_gdrive
from utils import count_files_and_folders
from googleapiclient.errors import HttpError

def count_recursive(source_folder_id):
    """Generate a report that shows the number of child objects (recursively) for each
    top-level folder under the source folder id and a total of nested folders for the
    source folder."""
    service = authenticate_gdrive()

    def execute_with_backoff(request):
        """Execute a request with exponential backoff in case of rate limits (429 or 403 errors)."""
        retries = 0
        while retries < 5:
            try:
                return request.execute()
            except HttpError as error:
                if error.resp.status in [403, 429]:  # Rate limiting errors
                    wait_time = (2 ** retries) + (0.1 * retries)  # Exponential backoff
                    print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                else:
                    raise  # Raise the error if it's not related to rate limits
        raise Exception("Exceeded maximum retries due to rate limits.")

    def list_files_with_pagination(folder_id):
        """List all files and folders inside the current folder with pagination to handle large results."""
        files = []
        page_token = None
        while True:
            query = f"'{folder_id}' in parents and trashed=false"
            response = service.files().list(
                q=query,
                fields="nextPageToken, files(id, mimeType, name)",
                pageToken=page_token
            )
            result = execute_with_backoff(response)
            files.extend(result.get('files', []))
            page_token = result.get('nextPageToken')
            if not page_token:
                break
        return files

    def count_children(folder_id):
        """Count all the files and folders inside the subfolder.
        Recursively call itself for any nested subfolders inside that subfolder."""
        # Get the initial file and folder counts for the current folder
        file_count, folder_count = count_files_and_folders(service, folder_id)

        nested_folder_count = folder_count
        
        # List all files and folders inside the current folder (with pagination)
        files = list_files_with_pagination(folder_id)

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
    count_recursive(source_folder_id)
