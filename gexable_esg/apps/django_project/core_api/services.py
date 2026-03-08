from uuid import uuid4

from gexable_esg.modules.data_foundation.service import DataIntakeService
from gexable_esg.modules.emissions.service import CalculationService
from gexable_esg.modules.governance.service import GovernanceService
from gexable_esg.modules.reporting.service import ReportingService
from gexable_esg.platform.event_bus.bus import InMemoryEventBus

from .repositories import ActivityRecordRepository, AuditLogRepository, DisclosureRepository, EmissionResultRepository

bus = InMemoryEventBus()
data_intake = DataIntakeService(event_bus=bus)
calculation = CalculationService(event_bus=bus)
reporting = ReportingService(event_bus=bus)
governance = GovernanceService(event_bus=bus)

activity_records = ActivityRecordRepository()
emission_results = EmissionResultRepository()
disclosures = DisclosureRepository()
audit_logs = AuditLogRepository()


def tenant_id_from_headers(request) -> str:
    return getattr(request, "tenant_id", request.headers.get("X-Tenant-ID", "default"))


def idempotency_key_from_headers(request) -> str:
    return request.headers.get("Idempotency-Key", str(uuid4()))
