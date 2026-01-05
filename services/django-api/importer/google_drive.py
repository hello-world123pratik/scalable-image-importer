from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
import os

API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_DRIVE_API_KEY not set")


def get_drive_service():
    return build("drive", "v3", developerKey=API_KEY)


def list_files_in_folder(folder_id):
    service = get_drive_service()

    query = f"'{folder_id}' in parents and mimeType contains 'image/'"

    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, size)",
        pageSize=1000,
        supportsAllDrives=True,
    ).execute()

    return results.get("files", [])


def download_file(file_id):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)

    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    fh.seek(0)
    return fh
