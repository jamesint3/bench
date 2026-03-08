from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DataSource, ImportFile, ImportJob, ValidationIssue


class ImportViewSet(viewsets.ViewSet):
    def list(self, request):
        jobs = ImportJob.objects.all().values("id", "source_id", "status", "started_at", "completed_at", "row_count")
        return Response(list(jobs))

    def retrieve(self, request, pk=None):
        job = ImportJob.objects.filter(pk=pk).values("id", "source_id", "status", "started_at", "completed_at", "row_count").first()
        if not job:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        files = list(ImportFile.objects.filter(import_job_id=pk).values("id", "file_name", "file_uri", "checksum"))
        issues = list(ValidationIssue.objects.filter(import_job_id=pk).values("id", "severity", "row_number", "field_name", "message"))
        return Response({"job": job, "files": files, "issues": issues})

    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request):
        source = DataSource.objects.first()
        if not source:
            source = DataSource.objects.create(tenant_id=request.data.get("tenant_id", "00000000-0000-0000-0000-000000000000"), name="default", source_type="csv")
        job = ImportJob.objects.create(tenant_id=source.tenant_id, source=source, status="pending")
        ImportFile.objects.create(
            tenant_id=source.tenant_id,
            import_job=job,
            file_name=request.data.get("file_name", "upload.csv"),
            file_uri=request.data.get("file_uri", "s3://uploads/upload.csv"),
        )
        return Response({"job_id": job.id, "status": job.status}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="validate")
    def validate(self, request):
        job_id = request.data.get("job_id")
        job = ImportJob.objects.filter(pk=job_id).first()
        if not job:
            return Response({"detail": "job not found"}, status=status.HTTP_404_NOT_FOUND)
        job.status = "running"
        job.save(update_fields=["status", "updated_at"])
        return Response({"job_id": job.id, "status": "validated"})

    @action(detail=False, methods=["post"], url_path="process")
    def process(self, request):
        job_id = request.data.get("job_id")
        job = ImportJob.objects.filter(pk=job_id).first()
        if not job:
            return Response({"detail": "job not found"}, status=status.HTTP_404_NOT_FOUND)
        job.status = "succeeded"
        job.save(update_fields=["status", "updated_at"])
        return Response({"job_id": job.id, "status": "processed"})
