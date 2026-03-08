from dataclasses import dataclass


@dataclass(slots=True)
class Organization:
    id: str
    name: str


@dataclass(slots=True)
class Site:
    id: str
    organization_id: str
    name: str
    country_code: str
