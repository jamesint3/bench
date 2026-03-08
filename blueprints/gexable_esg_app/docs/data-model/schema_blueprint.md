# Database schema blueprint (MVP-first)

## Core

- tenants
- users
- user_tenant_memberships
- roles

## Operational

- sites
- meters
- utility_bills_raw
- meter_readings_raw (timeseries)
- emission_factor_library

## Analytics

- fact_energy_consumption_daily
- fact_emissions_monthly
- kpi_emissions_overview
- kpi_energy_site_monthly

## Workflow

- decarbonization_projects
- audits
- audit_findings
- corrective_actions
