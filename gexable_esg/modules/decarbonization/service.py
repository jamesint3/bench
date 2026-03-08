class DecarbonizationService:
    def evaluate_project(self, annual_co2e_reduction_kg: float, annual_cost_usd: float) -> dict:
        mac = annual_cost_usd / annual_co2e_reduction_kg if annual_co2e_reduction_kg else 0.0
        return {
            "annual_co2e_reduction_kg": annual_co2e_reduction_kg,
            "annual_cost_usd": annual_cost_usd,
            "marginal_abatement_cost": round(mac, 4),
        }
