from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class DomainEvent:
    topic: str
    payload: dict[str, Any]
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "v1"

    def model_dump(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "payload": self.payload,
            "occurred_at": self.occurred_at.isoformat(),
            "schema_version": self.schema_version,
        }


class InMemoryEventBus:
    def __init__(self) -> None:
        self.events: list[DomainEvent] = []

    def publish(self, topic: str, payload: dict[str, Any], schema_version: str = "v1") -> DomainEvent:
        event = DomainEvent(topic=topic, payload=payload, schema_version=schema_version)
        self.events.append(event)
        return event
