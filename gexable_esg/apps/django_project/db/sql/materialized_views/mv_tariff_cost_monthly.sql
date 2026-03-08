CREATE MATERIALIZED VIEW IF NOT EXISTS mv_tariff_cost_monthly AS
SELECT
    tenant_id,
    site_id,
    date_trunc('month', date)::date AS month_start,
    SUM(energy_charge) AS energy_charge,
    SUM(demand_charge) AS demand_charge,
    SUM(fixed_charge) AS fixed_charge,
    SUM(other_charge) AS other_charge,
    SUM(total_cost) AS total_cost,
    MIN(currency) AS currency
FROM fact_tariff_costs
GROUP BY tenant_id, site_id, date_trunc('month', date)::date;

CREATE INDEX IF NOT EXISTS mv_tariff_cost_monthly_tenant_month_idx
    ON mv_tariff_cost_monthly (tenant_id, month_start, site_id);
