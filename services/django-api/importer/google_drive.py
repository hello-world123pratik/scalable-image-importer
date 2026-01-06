from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from io import BytesIO
import os


def get_drive_service():
    """
    Create Google Drive service using API key.
    Works ONLY for PUBLIC folders/files.
    """
    api_key = os.getenv("GOOGLE_DRIVE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_DRIVE_API_KEY not set")

    return build(
        "drive",
        "v3",
        developerKey=api_key,
        cache_discovery=False,
    )


def list_files_in_folder(folder_id):
    """
    List all image files in a Google Drive folder.
    Folder MUST be public.
    """
    if not folder_id:
        raise ValueError("folder_id is required")

    service = get_drive_service()

    query = f"'{folder_id}' in parents and mimeType contains 'image/'"

    try:
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, size)",
            pageSize=1000,
            supportsAllDrives=True,
        ).execute()

        return results.get("files", [])

    except HttpError as e:
        raise RuntimeError(f"Google Drive API error: {e}")


def download_file(file_id):
    """
    Download a single file from Google Drive into memory.
    File MUST be public.
    """
    if not file_id:
        raise ValueError("file_id is required")

    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)

    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    try:
        done = False
        while not done:
            _, done = downloader.next_chunk()

        fh.seek(0)
        return fh

    except HttpError as e:
        raise RuntimeError(f"Google Drive download error: {e}")
