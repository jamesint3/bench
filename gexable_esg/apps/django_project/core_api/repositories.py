from datetime import timezone, datetime
from decimal import Decimal

from .models import ActivityRecord, AuditLog, DisclosureReport, DomainEventOutbox, EmissionResult


class ActivityRecordRepository:
    def create(
        self,
        *,
        tenant_id: str,
        site_id: int,
        quantity: float,
        unit: str,
        source_type: str,
        idempotency_key: str,
    ) -> ActivityRecord:
        return ActivityRecord.objects.create(
            tenant_id=tenant_id,
            site_id=site_id,
            quantity=Decimal(str(quantity)),
            unit=unit,
            source_type=source_type,
            idempotency_key=idempotency_key,
        )

    def for_tenant(self, tenant_id: str):
        return ActivityRecord.objects.filter(tenant_id=tenant_id)


class EmissionResultRepository:
    def create(
        self,
        *,
        tenant_id: str,
        activity_record_id: int,
        scope: str,
        co2e_kg: float,
        calculation_method_version: str,
        factor_version: str,
    ) -> EmissionResult:
        return EmissionResult.objects.create(
            tenant_id=tenant_id,
            activity_record_id=activity_record_id,
            scope=scope,
            co2e_kg=Decimal(str(co2e_kg)),
            calculation_method_version=calculation_method_version,
            factor_version=factor_version,
        )

    def for_tenant(self, tenant_id: str):
        return EmissionResult.objects.filter(tenant_id=tenant_id)


class DisclosureRepository:
    def create(self, *, tenant_id: str, framework: str, period: str, status: str) -> DisclosureReport:
        return DisclosureReport.objects.create(
            tenant_id=tenant_id,
            framework=framework,
            period=period,
            status=status,
        )

    def for_tenant(self, tenant_id: str):
        return DisclosureReport.objects.filter(tenant_id=tenant_id)


class AuditLogRepository:
    def log(self, *, tenant_id: str, action: str, entity_type: str, entity_id: str, payload: dict) -> AuditLog:
        return AuditLog.objects.create(
            tenant_id=tenant_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )


class DomainEventOutboxRepository:
    def queue(self, *, tenant_id: str, topic: str, payload: dict, schema_version: str = "v1") -> DomainEventOutbox:
        return DomainEventOutbox.objects.create(
            tenant_id=tenant_id,
            topic=topic,
            payload=payload,
            schema_version=schema_version,
            status="pending",
        )

    def get_pending(self, *, batch_size: int = 100):
        return DomainEventOutbox.objects.filter(status="pending").order_by("id")[:batch_size]

    def mark_published(self, event_id: int) -> None:
        DomainEventOutbox.objects.filter(id=event_id).update(
            status="published",
            published_at=datetime.now(timezone.utc),
            error_message=None,
        )

    def mark_error(self, event_id: int, message: str) -> None:
        DomainEventOutbox.objects.filter(id=event_id).update(status="error", error_message=message)
