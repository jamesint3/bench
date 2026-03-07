from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass(slots=True)
class DisclosureReport:
    id: str
    framework: str
    period: str
    status: str
    published_at: datetime

    def model_dump(self) -> dict:
        return {
            "id": self.id,
            "framework": self.framework,
            "period": self.period,
            "status": self.status,
            "published_at": self.published_at.isoformat(),
        }


def build_disclosure_report(report_id: str, framework: str, period: str) -> DisclosureReport:
    return DisclosureReport(
        id=report_id,
        framework=framework,
        period=period,
        status="published",
        published_at=datetime.now(UTC),
    )
