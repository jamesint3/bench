from uuid import uuid4

from gexable_esg.modules.data_foundation.models import ActivityRecord, build_activity_record
from gexable_esg.platform.event_bus.bus import InMemoryEventBus


class DataIntakeService:
    def __init__(self, event_bus: InMemoryEventBus) -> None:
        self.event_bus = event_bus

    def ingest(self, payload: dict) -> ActivityRecord:
        record = build_activity_record(record_id=str(uuid4()), payload=payload)
        self.event_bus.publish("activity_record.ingested", record.model_dump())
        self.event_bus.publish(
            "activity_record.validated",
            {"activity_record_id": record.id, "status": "valid"},
        )
        return record
