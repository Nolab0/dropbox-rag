import dropboxDriver
from dropbox.exceptions import AuthError

def connect_to_dropbox():
    """Connect to Dropbox and return the client."""
    try:
        dbx = dropboxDriver.Dropbox(os.getenv("DROPBOX_ACCESS_TOKEN"))
        dbx.users_get_current_account()
        print("Connected to Dropbox successfully.")
        return dbx
    except AuthError as e:
        print("Dropbox authentication failed: ", e)
        return None
    

def list_files(dbx, folder_path=""):
    """List files in a Dropbox folder."""
    try:
        response = dbx.files_list_folder(folder_path)
        return [entry for entry in response.entries if isinstance(entry, dropboxDriver.files.FileMetadata)]
    except Exception as e:
        print(f"Error listing files: {e}")
        return []
    

def download_file(dbx, path):
    """Download a file from Dropbox."""
    try:
        metadata, res = dbx.files_download(path)
        return res.content
    except Exception as e:
        print(f"Error downloading file {path}: {e}")
        return None