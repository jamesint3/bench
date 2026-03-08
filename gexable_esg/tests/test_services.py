from gexable_esg.modules.decarbonization.service import DecarbonizationService
from gexable_esg.modules.performance.service import PerformanceService
from gexable_esg.modules.supplier.service import SupplierService


def test_performance_energy_intensity() -> None:
    service = PerformanceService()
    assert service.energy_intensity(1000, 50) == 20.0


def test_supplier_quality_score() -> None:
    service = SupplierService()
    assert service.quality_score(80, 90) == 84.0


def test_decarbonization_mac() -> None:
    service = DecarbonizationService()
    result = service.evaluate_project(1000, 250)
    assert result["marginal_abatement_cost"] == 0.25
