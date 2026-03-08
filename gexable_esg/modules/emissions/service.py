from gexable_esg.modules.emissions.models import EmissionFactor, EmissionResult
from gexable_esg.platform.event_bus.bus import InMemoryEventBus


class CalculationService:
    DEFAULT_FACTOR = EmissionFactor(code="GRID_ELECTRICITY", unit="kWh", co2e_per_unit=0.42)

    def __init__(self, event_bus: InMemoryEventBus) -> None:
        self.event_bus = event_bus

    def calculate(self, payload: dict) -> EmissionResult:
        quantity = float(payload["quantity"])
        factor = float(payload.get("factor", self.DEFAULT_FACTOR.co2e_per_unit))
        result = EmissionResult(
            activity_record_id=payload.get("activity_record_id", "unknown"),
            scope=payload.get("scope", "scope2"),
            co2e_kg=round(quantity * factor, 4),
        )
        self.event_bus.publish("emission_result.calculated", result.model_dump())
        return result
