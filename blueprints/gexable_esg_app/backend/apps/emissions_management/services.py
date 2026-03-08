from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from .models import EmissionFactor, EmissionRecord, EmissionSource


@dataclass
class EmissionCalculationInput:
    tenant_id: str
    source: EmissionSource
    factor: EmissionFactor
    activity_date: str
    activity_amount: Decimal
    activity_unit: str


class EmissionCalculationService:
    """Write/business logic for emission calculations and record lifecycle."""

    @staticmethod
    @transaction.atomic
    def calculate_and_store(payload: EmissionCalculationInput) -> EmissionRecord:
        emissions_tco2e = payload.activity_amount * payload.factor.factor_value
        return EmissionRecord.all_objects.create(
            tenant_id=payload.tenant_id,
            source=payload.source,
            factor=payload.factor,
            activity_date=payload.activity_date,
            activity_amount=payload.activity_amount,
            activity_unit=payload.activity_unit,
            emissions_tco2e=emissions_tco2e,
        )

    @staticmethod
    @transaction.atomic
    def recalculate_with_factor(record: EmissionRecord, factor: EmissionFactor) -> EmissionRecord:
        record.factor = factor
        record.emissions_tco2e = record.activity_amount * factor.factor_value
        record.save(update_fields=["factor", "emissions_tco2e", "updated_at"])
        return record
