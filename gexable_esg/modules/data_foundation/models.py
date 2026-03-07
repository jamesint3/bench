from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass(slots=True)
class ActivityRecord:
    id: str
    site_id: str
    quantity: float
    unit: str
    source_type: str
    recorded_at: datetime

    def model_dump(self) -> dict:
        return {
            "id": self.id,
            "site_id": self.site_id,
            "quantity": self.quantity,
            "unit": self.unit,
            "source_type": self.source_type,
            "recorded_at": self.recorded_at.isoformat(),
        }


def build_activity_record(record_id: str, payload: dict) -> ActivityRecord:
    return ActivityRecord(
        id=record_id,
        site_id=payload["site_id"],
        quantity=float(payload["quantity"]),
        unit=payload.get("unit", "kWh"),
        source_type=payload.get("source_type", "manual_upload"),
        recorded_at=datetime.now(UTC),
    )
