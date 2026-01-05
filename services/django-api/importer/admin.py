from django.contrib import admin
from .models import ImportJob, Image


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source",
        "status",
        "total_items",
        "processed_items",
        "created_at",
        "updated_at",
    )

    list_filter = ("status", "source", "created_at")
    search_fields = ("source_url", "error_message")

    readonly_fields = (
        "source_url",
        "source",
        "total_items",
        "processed_items",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Job Info", {
            "fields": ("source", "source_url", "status")
        }),
        ("Progress", {
            "fields": ("total_items", "processed_items")
        }),
        ("Errors", {
            "fields": ("error_message",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size",
        "mime_type",
        "source",
        "created_at",
    )

    list_filter = ("source", "mime_type", "created_at")
    search_fields = ("name", "google_drive_id")

    readonly_fields = (
        "name",
        "google_drive_id",
        "size",
        "mime_type",
        "storage_path",
        "source",
        "created_at",
    )

    ordering = ("-created_at",)
