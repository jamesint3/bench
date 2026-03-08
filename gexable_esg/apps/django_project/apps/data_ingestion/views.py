from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.request_context import get_tenant_id

from .models import DataSource, ImportFile, ImportJob, ValidationIssue


class ImportViewSet(viewsets.ViewSet):
    def list(self, request):
        tenant_id = get_tenant_id(request)
        jobs = ImportJob.objects.filter(tenant_id=tenant_id) if tenant_id else ImportJob.objects.none()
        return Response(list(jobs.values("id", "source_id", "status", "started_at", "completed_at", "row_count")))

    def retrieve(self, request, pk=None):
        tenant_id = get_tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)

        job = (
            ImportJob.objects.filter(pk=pk, tenant_id=tenant_id)
            .values("id", "source_id", "status", "started_at", "completed_at", "row_count")
            .first()
        )
        if not job:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        files = list(
            ImportFile.objects.filter(import_job_id=pk, tenant_id=tenant_id).values("id", "file_name", "file_uri", "checksum")
        )
        issues = list(
            ValidationIssue.objects.filter(import_job_id=pk, tenant_id=tenant_id).values(
                "id", "severity", "row_number", "field_name", "message"
            )
        )
        return Response({"job": job, "files": files, "issues": issues})

    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request):
        tenant_id = get_tenant_id(request)
        if not tenant_id:
            return Response({"detail": "tenant context required"}, status=status.HTTP_400_BAD_REQUEST)

        source = DataSource.objects.filter(tenant_id=tenant_id).first()
        if not source:
            source = DataSource.objects.create(tenant_id=tenant_id, name="default", source_type="csv")
        job = ImportJob.objects.create(tenant_id=tenant_id, source=source, status="pending")
        ImportFile.objects.create(
            tenant_id=tenant_id,
            import_job=job,
            file_name=request.data.get("file_name", "upload.csv"),
            file_uri=request.data.get("file_uri", "s3://uploads/upload.csv"),
        )
        return Response({"job_id": job.id, "status": job.status}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="validate")
    def validate(self, request):
        tenant_id = get_tenant_id(request)
        job_id = request.data.get("job_id")
        job = ImportJob.objects.filter(pk=job_id, tenant_id=tenant_id).first() if tenant_id else None
        if not job:
            return Response({"detail": "job not found"}, status=status.HTTP_404_NOT_FOUND)
        job.status = "running"
        job.save(update_fields=["status", "updated_at"])
        return Response({"job_id": job.id, "status": "validated"})

    @action(detail=False, methods=["post"], url_path="process")
    def process(self, request):
        tenant_id = get_tenant_id(request)
        job_id = request.data.get("job_id")
        job = ImportJob.objects.filter(pk=job_id, tenant_id=tenant_id).first() if tenant_id else None
        if not job:
            return Response({"detail": "job not found"}, status=status.HTTP_404_NOT_FOUND)
        job.status = "succeeded"
        job.save(update_fields=["status", "updated_at"])
        return Response({"job_id": job.id, "status": "processed"})
