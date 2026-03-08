CREATE MATERIALIZED VIEW IF NOT EXISTS mv_supplier_rankings AS
SELECT
    f.tenant_id,
    f.supplier_id,
    s.name AS supplier_name,
    f.period_start,
    f.period_end,
    SUM(f.emissions_tco2e) AS emissions_tco2e,
    AVG(f.data_quality_score) AS data_quality_score,
    DENSE_RANK() OVER (
        PARTITION BY f.tenant_id, f.period_start, f.period_end
        ORDER BY SUM(f.emissions_tco2e) DESC
    ) AS emissions_rank
FROM fact_supplier_emissions f
JOIN suppliers s ON s.id = f.supplier_id
GROUP BY f.tenant_id, f.supplier_id, s.name, f.period_start, f.period_end;

CREATE INDEX IF NOT EXISTS mv_supplier_rankings_tenant_period_idx
    ON mv_supplier_rankings (tenant_id, period_start, period_end, emissions_rank);
