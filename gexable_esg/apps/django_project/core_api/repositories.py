from decimal import Decimal

from .models import ActivityRecord, AuditLog, DisclosureReport, EmissionResult


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


class DisclosureRepository:
    def create(self, *, tenant_id: str, framework: str, period: str, status: str) -> DisclosureReport:
        return DisclosureReport.objects.create(
            tenant_id=tenant_id,
            framework=framework,
            period=period,
            status=status,
        )


class AuditLogRepository:
    def log(self, *, tenant_id: str, action: str, entity_type: str, entity_id: str, payload: dict) -> AuditLog:
        return AuditLog.objects.create(
            tenant_id=tenant_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )
