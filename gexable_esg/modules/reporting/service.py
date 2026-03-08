from uuid import uuid4

from gexable_esg.modules.reporting.models import DisclosureReport, build_disclosure_report
from gexable_esg.platform.event_bus.bus import InMemoryEventBus


class ReportingService:
    def __init__(self, event_bus: InMemoryEventBus) -> None:
        self.event_bus = event_bus

    def publish(self, payload: dict) -> DisclosureReport:
        report = build_disclosure_report(
            report_id=str(uuid4()),
            framework=payload.get("framework", "CSRD"),
            period=payload.get("period", "2026-Q1"),
        )
        self.event_bus.publish("disclosure.report_published", report.model_dump())
        return report
