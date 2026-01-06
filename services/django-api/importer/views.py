from django.http import JsonResponse
from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters

from .models import ImportJob, Image
from .serializers import ImageSerializer
from .schemas import GoogleDriveImportRequest
from .tasks import process_google_drive_folder
from .redis_limit import check_rate_limit


class GoogleDriveImportView(APIView):
    """
    Start a Google Drive import job.
    """

    def post(self, request):
        try:
            payload = GoogleDriveImportRequest(**request.data)
        except Exception as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        folder_url = str(payload.url)

        # Rate limit check (by URL, not ID)
        if not check_rate_limit(folder_url):
            return Response(
                {"error": "Rate limit exceeded for this folder"},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        job = ImportJob.objects.create(
            source_url=folder_url,
            status="queued",
        )

        # ✅ IMPORTANT: pass FULL URL to Celery
        process_google_drive_folder.delay(job.id, folder_url)

        return Response(
            {
                "job_id": job.id,
                "status": job.status,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class JobStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ImportJob.objects.get(id=job_id)
        except ImportJob.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "job_id": job.id,
                "status": job.status,
                "processed_items": job.processed_items,
                "total_items": job.total_items,
            }
        )


class ImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "google_drive_id"]

    def get_queryset(self):
        queryset = Image.objects.all().order_by("-created_at")
        source = self.request.query_params.get("source")
        if source:
            queryset = queryset.filter(source=source)
        return queryset


class HealthCheckView(APIView):
    def get(self, request):
        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1;")
        except Exception:
            return Response(
                {"status": "db_error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"status": "ok"})


def home(request):
    return JsonResponse(
        {"message": "Welcome to Scalable Image Importer API"}
    )
