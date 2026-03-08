from dataclasses import dataclass


@dataclass(slots=True)
class TenantContext:
    tenant_id: str
    region: str
    row_level_security_enabled: bool = True
