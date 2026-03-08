CREATE MATERIALIZED VIEW IF NOT EXISTS mv_energy_site_comparison AS
SELECT
    f.tenant_id,
    f.site_id,
    s.name AS site_name,
    date_trunc('month', f.date)::date AS month_start,
    SUM(f.energy_kwh) AS total_energy_kwh,
    AVG(f.peak_kw) AS avg_peak_kw,
    SUM(f.renewable_kwh) AS renewable_kwh,
    CASE WHEN SUM(f.energy_kwh) > 0
         THEN (SUM(f.renewable_kwh) / SUM(f.energy_kwh)) * 100
         ELSE NULL END AS renewable_share_pct
FROM fact_energy_consumption_daily f
JOIN sites s ON s.id = f.site_id
GROUP BY f.tenant_id, f.site_id, s.name, date_trunc('month', f.date)::date;

CREATE INDEX IF NOT EXISTS mv_energy_site_comparison_tenant_month_idx
    ON mv_energy_site_comparison (tenant_id, month_start, site_id);
