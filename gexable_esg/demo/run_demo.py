import json
from dataclasses import asdict, dataclass

from gexable_esg.modules.data_foundation.service import DataIntakeService
from gexable_esg.modules.emissions.service import CalculationService
from gexable_esg.modules.governance.service import GovernanceService
from gexable_esg.modules.reporting.service import ReportingService
from gexable_esg.platform.event_bus.bus import InMemoryEventBus


@dataclass(slots=True)
class DemoResult:
    activity_record: dict
    emission_result: dict
    disclosure_report: dict
    control_exception: dict
    events: list[dict]


def run_demo() -> DemoResult:
    bus = InMemoryEventBus()

    data_intake = DataIntakeService(event_bus=bus)
    calculation = CalculationService(event_bus=bus)
    reporting = ReportingService(event_bus=bus)
    governance = GovernanceService(event_bus=bus)

    record = data_intake.ingest(
        {
            "site_id": "site-berlin-01",
            "quantity": 1200,
            "unit": "kWh",
            "source_type": "utility_bill",
        }
    )

    emission = calculation.calculate(
        {
            "activity_record_id": record.id,
            "quantity": record.quantity,
            "scope": "scope2",
        }
    )

    disclosure = reporting.publish(
        {
            "framework": "CSRD",
            "period": "2026-Q1",
        }
    )

    control = governance.record_control_exception(
        control_id="ctrl-disclosure-review",
        message="Demo exception: reviewer evidence missing",
    )

    return DemoResult(
        activity_record=record.model_dump(),
        emission_result=emission.model_dump(),
        disclosure_report=disclosure.model_dump(),
        control_exception=control,
        events=[e.model_dump() for e in bus.events],
    )


def main() -> None:
    result = run_demo()
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
