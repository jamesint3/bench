class InsightsService:
    def detect_hotspot(self, location_emission_kg: float, org_average_kg: float) -> bool:
        if org_average_kg <= 0:
            return False
        return location_emission_kg > (org_average_kg * 1.25)
