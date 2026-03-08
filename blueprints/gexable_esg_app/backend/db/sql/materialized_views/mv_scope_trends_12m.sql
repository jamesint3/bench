CREATE MATERIALIZED VIEW IF NOT EXISTS mv_scope_trends_12m AS
SELECT
    tenant_id,
    scope,
    date_trunc('month', make_date(year, month, 1))::date AS month_start,
    SUM(emissions_tco2e) AS emissions_tco2e
FROM fact_emissions_monthly
WHERE make_date(year, month, 1) >= date_trunc('month', CURRENT_DATE) - INTERVAL '11 months'
GROUP BY tenant_id, scope, date_trunc('month', make_date(year, month, 1))::date;

CREATE INDEX IF NOT EXISTS mv_scope_trends_12m_tenant_scope_month_idx
    ON mv_scope_trends_12m (tenant_id, scope, month_start);
