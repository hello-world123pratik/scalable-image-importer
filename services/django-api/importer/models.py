from django.db import models


class ImportJob(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    source_url = models.URLField()
    source = models.CharField(max_length=20, default="google_drive")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="queued"
    )
    total_items = models.PositiveIntegerField(default=0)
    processed_items = models.PositiveIntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    name = models.CharField(max_length=255)
    google_drive_id = models.CharField(max_length=100, unique=True)
    size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    storage_path = models.URLField()
    source = models.CharField(max_length=20, default="google_drive")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["google_drive_id"]),
            models.Index(fields=["source"]),
            models.Index(fields=["created_at"]),
        ]
