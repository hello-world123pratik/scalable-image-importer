from django.urls import path
from .views import (
    home,
    GoogleDriveImportView,
    ImageListView,
    JobStatusView,
    HealthCheckView,
)

urlpatterns = [
    path("", home, name="home"),
    path("import/google-drive", GoogleDriveImportView.as_view(), name="google_drive_import"),
    path("images", ImageListView.as_view(), name="image_list"),
    path("jobs/<int:job_id>", JobStatusView.as_view(), name="job_status"),
    path("health/", HealthCheckView.as_view(), name="health_check"),
]
