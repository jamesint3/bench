from __future__ import annotations

from uuid import UUID

from .models import ExportJob, ReportRun, ReportTemplate


def list_templates(*, tenant_id: UUID):
    return ReportTemplate.objects.filter(tenant_id=tenant_id).values(
        "id", "name", "framework", "file_format", "template_config", "created_at", "updated_at"
    )


def list_report_runs(*, tenant_id: UUID):
    return ReportRun.objects.filter(tenant_id=tenant_id).values(
        "id", "template_id", "requested_by_id", "status", "output_uri", "started_at", "completed_at"
    )


def list_export_jobs(*, tenant_id: UUID):
    return ExportJob.objects.filter(tenant_id=tenant_id).values(
        "id", "report_run_id", "export_type", "status", "artifact_uri", "created_at", "updated_at"
    )
