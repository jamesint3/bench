from dataclasses import dataclass


@dataclass(slots=True)
class EmissionFactor:
    code: str
    unit: str
    co2e_per_unit: float


@dataclass(slots=True)
class EmissionResult:
    activity_record_id: str
    scope: str
    co2e_kg: float

    def model_dump(self) -> dict:
        return {
            "activity_record_id": self.activity_record_id,
            "scope": self.scope,
            "co2e_kg": self.co2e_kg,
        }
