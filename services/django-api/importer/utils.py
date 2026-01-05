import re

def extract_drive_folder_id(value: str) -> str:
    """
    Extract Google Drive folder ID from:
    - Full folder URLs (with /folders/ or /open?id=)
    - URLs with query parameters (?usp=...)
    - Raw folder IDs
    """
    if not value:
        raise ValueError("Empty Google Drive folder value")

    value = value.strip()

    # Strip query parameters
    value = value.split('?')[0]

    # Try /folders/<id> pattern
    match = re.search(r"/folders/([a-zA-Z0-9_-]+)", value)
    if match:
        return match.group(1)

    # Try /open?id=<id> pattern
    match = re.search(r"open\?id=([a-zA-Z0-9_-]+)", value)
    if match:
        return match.group(1)

    # Try raw ID (Google Drive IDs are usually 20-50 chars)
    if re.fullmatch(r"[a-zA-Z0-9_-]{20,50}", value):
        return value

    raise ValueError(f"Invalid Google Drive folder URL or ID: {value}")
