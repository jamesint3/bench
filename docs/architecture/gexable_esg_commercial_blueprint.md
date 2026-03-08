# Gexable ESG Commercial Architecture Blueprint

This document maps the target architecture for a commercial ESG/energy analytics product while preserving the current implementation.

## High-level layers

1. Frontend (React dashboards, role-aware pages, chart/table components)
2. API/Application layer (Django + DRF endpoints)
3. Operational business logic (services/selectors)
4. Background analytics (Celery workers + schedules)
5. Redis (broker/cache)
6. Data layer (PostgreSQL + TimescaleDB)
7. Analytics/modeling (Pandas/NumPy/Statsmodels)
8. Reporting extensions (optional BI)

## Design rule

Always flow:

- raw ingestion tables
- processing and normalization jobs
- fact + KPI summary + materialized views
- API-ready query layer
- dashboard delivery

Avoid direct dashboard reads from raw ingestion tables.

## Domain module map

- core
- tenants
- users
- permissions
- audit_log
- data_ingestion
- emissions_management
- energy_management
- decarbonization
- supplier_intelligence
- audits_actions
- analytics
- reporting
- dashboard_api

## First dashboard set

- emissions overview
- scope 1/2/3 trends
- energy by site
- audit findings/actions
- decarbonization tracker

## API endpoint blueprint

- `GET /api/dashboard/emissions-overview`
- `GET /api/dashboard/scope-trends`
- `GET /api/dashboard/energy-by-site`
- `GET /api/dashboard/tariff-analysis`
- `GET /api/dashboard/renewable-performance`
- `GET /api/dashboard/decarbonization-projects`
- `GET /api/dashboard/supplier-benchmarking`
- `GET /api/dashboard/audit-actions`

## Implementation note

This blueprint is committed as documentation + scaffold under `blueprints/gexable_esg_app/` to avoid impacting active production code paths.
