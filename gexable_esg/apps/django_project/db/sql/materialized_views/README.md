# Materialized views (dashboard-ready)

These views implement the recommended pattern:

- keep raw interval data in hypertables
- aggregate into fact/KPI layers
- serve dashboards from precomputed outputs, not raw interval tables

## Implemented views

- `mv_scope_trends_12m` — monthly rolling scope totals
- `mv_energy_site_comparison` — site-by-site monthly energy benchmark
- `mv_tariff_cost_monthly` — monthly cost breakdown by site
- `mv_supplier_rankings` — supplier emissions and quality ranking
- `mv_project_progress` — decarbonization status and achieved abatement
- `mv_audit_closure_trend` — finding closure rates over time

## Refresh guidance

Use `REFRESH MATERIALIZED VIEW CONCURRENTLY` in scheduled jobs where possible.
For heavy tenants, refresh incrementally by period partition strategy.
