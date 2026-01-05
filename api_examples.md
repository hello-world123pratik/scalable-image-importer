# API Usage Examples

Base URL (local):
http://localhost:8000

## 1️ Health Check

Checks database connectivity and service health.

curl http://localhost:8000/health/
Response:

{
  "status": "ok"
}

## 2️ Import Images from Google Drive Folder

Triggers an asynchronous import job using Celery.

curl -X POST http://localhost:8000/import/google-drive \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"
  }'
Response:

{
  "job_id": 1,
  "status": "queued"
}

## 3️ Check Import Job Status

curl http://localhost:8000/jobs/1
Response:

{
  "job_id": 1,
  "status": "completed"
}

## 4️ List Imported Images

Returns metadata for all imported images.

curl http://localhost:8000/images
Response:

[
  {
    "id": 1,
    "name": "image1.jpg",
    "google_drive_id": "abc123",
    "size": 204800,
    "mime_type": "image/jpeg",
    "storage_path": "http://minio:9000/images/image1.jpg",
    "source": "google_drive",
    "created_at": "2024-01-01T12:00:00Z"
  }
]
