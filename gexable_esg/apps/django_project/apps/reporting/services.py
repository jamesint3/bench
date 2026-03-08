from __future__ import annotations

from django.utils import timezone

from .models import ExportJob, ReportRecipient, ReportRun, ReportTemplate
from .tasks import generate_scheduled_report


def create_template(*, tenant_id, payload: dict, requested_by_id: int | None) -> ReportTemplate:
    return ReportTemplate.objects.create(
        tenant_id=tenant_id,
        name=payload["name"],
        framework=payload["framework"],
        file_format=payload.get("file_format", "pdf"),
        template_config=payload.get("template_config", {}),
    )


def create_report_run(*, tenant_id, payload: dict, requested_by_id: int | None) -> ReportRun:
    run = ReportRun.objects.create(
        tenant_id=tenant_id,
        template_id=payload["template_id"],
        requested_by_id=requested_by_id,
        status="pending",
        started_at=timezone.now(),
    )
    generate_scheduled_report.delay(run.id)
    return run


def create_export_job(*, tenant_id, payload: dict) -> ExportJob:
    return ExportJob.objects.create(
        tenant_id=tenant_id,
        report_run_id=payload["report_run_id"],
        export_type=payload.get("export_type", "csv"),
        status="pending",
    )


def deliver_report(*, tenant_id, report_run: ReportRun, emails: list[str]) -> dict[str, int]:
    created = 0
    for email in emails:
        ReportRecipient.objects.create(tenant_id=tenant_id, report_run=report_run, email=email, delivery_status="queued")
        created += 1
    report_run.status = "delivering"
    report_run.save(update_fields=["status", "updated_at"])
    return {"queued_recipients": created}
