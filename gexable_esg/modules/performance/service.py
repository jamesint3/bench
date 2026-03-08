class PerformanceService:
    def energy_intensity(self, total_energy_kwh: float, output_units: float) -> float:
        if output_units <= 0:
            raise ValueError("output_units must be greater than zero")
        return round(total_energy_kwh / output_units, 4)
