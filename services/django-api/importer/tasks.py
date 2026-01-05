import logging
import mimetypes

from celery import shared_task
from botocore.exceptions import ClientError
import boto3

from django.conf import settings
from .google_drive import list_files_in_folder, download_file
from .models import ImportJob, Image
from .utils import extract_drive_folder_id

logger = logging.getLogger(__name__)


# ------------------------
# S3 / MinIO client (INTERNAL)
# ------------------------
def get_s3_client():
    """
    Returns a boto3 S3 client configured for MinIO.
    Used ONLY by Django / Celery (inside Docker).
    """
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,  # http://minio:9000
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Ensure bucket exists
    try:
        s3.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    except ClientError:
        s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

    return s3


# ------------------------
# Public image URL (BROWSER)
# ------------------------
def get_image_url(object_key: str) -> str:
    """
    Returns a PUBLIC URL accessible by the browser / React app.
    Example:
    http://localhost:9002/images/images/abc123_file.jpg
    """
    public_endpoint = settings.AWS_S3_PUBLIC_URL.rstrip("/")
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    return f"{public_endpoint}/{bucket}/{object_key}"


# ------------------------
# Upload task
# ------------------------
@shared_task(bind=True, max_retries=5, queue="uploader")
def download_and_upload_image(self, job_id, file):
    """
    Download a file from Google Drive and upload it to MinIO.
    Saves a PUBLIC URL in the database.
    """
    try:
        s3 = get_s3_client()

        # Download from Google Drive
        file_obj = download_file(file["id"])
        file_obj.seek(0, 2)
        file_size = file_obj.tell()
        file_obj.seek(0)

        mime_type = (
            file.get("mimeType")
            or mimetypes.guess_type(file["name"])[0]
            or "application/octet-stream"
        )

        object_key = f"images/{file['id']}_{file['name']}"

        # Upload to MinIO
        s3.upload_fileobj(
            Fileobj=file_obj,
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=object_key,
            ExtraArgs={"ContentType": mime_type},
        )

        # PUBLIC URL (important fix)
        storage_path = get_image_url(object_key)

        image, created = Image.objects.get_or_create(
            google_drive_id=file["id"],
            defaults={
                "name": file["name"],
                "size": file_size,
                "mime_type": mime_type,
                "storage_path": storage_path,
                "source": "google_drive",
            },
        )

        if created:
            logger.info(f"Uploaded new image: {file['name']} ({file['id']})")
        else:
            logger.info(f"Image already exists: {file['name']} ({file['id']})")

        # Update job progress
        job = ImportJob.objects.get(id=job_id)
        job.processed_items += 1
        if job.processed_items >= job.total_items:
            job.status = "completed"
        job.save(update_fields=["processed_items", "status"])

        return file["id"]

    except Exception as exc:
        logger.exception("Upload failed")
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


# ------------------------
# Importer task
# ------------------------
@shared_task(queue="importer")
def process_google_drive_folder(job_id, folder_url):
    """
    Fetch all image files from a Google Drive folder
    and queue them for upload.
    """
    logger.info(f"Job {job_id} started")

    try:
        folder_id = extract_drive_folder_id(folder_url)

        ImportJob.objects.filter(id=job_id).update(
            status="running",
            processed_items=0,
        )

        files = list_files_in_folder(folder_id)
        ImportJob.objects.filter(id=job_id).update(
            total_items=len(files)
        )

        if not files:
            ImportJob.objects.filter(id=job_id).update(status="completed")
            return "No images found"

        for f in files:
            download_and_upload_image.delay(job_id, f)

        return "Import started"

    except Exception as exc:
        logger.exception("Job failed")
        ImportJob.objects.filter(id=job_id).update(
            status="failed",
            error_message=str(exc),
        )
        raise
