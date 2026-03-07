from gexable_esg.modules.data_foundation.service import DataIntakeService
from gexable_esg.modules.emissions.service import CalculationService
from gexable_esg.modules.governance.service import GovernanceService
from gexable_esg.modules.reporting.service import ReportingService
from gexable_esg.platform.event_bus.bus import InMemoryEventBus

bus = InMemoryEventBus()
data_intake = DataIntakeService(event_bus=bus)
calculation = CalculationService(event_bus=bus)
reporting = ReportingService(event_bus=bus)
governance = GovernanceService(event_bus=bus)
