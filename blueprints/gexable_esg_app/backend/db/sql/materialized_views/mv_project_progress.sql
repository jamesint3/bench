CREATE MATERIALIZED VIEW IF NOT EXISTS mv_project_progress AS
SELECT
    p.tenant_id,
    p.id AS project_id,
    p.name,
    p.category,
    p.status,
    p.planned_start_date,
    p.planned_end_date,
    p.expected_abatement_tco2e,
    p.actual_abatement_tco2e,
    COALESCE(SUM(a.actual_abatement_tco2e), 0) AS abatement_recorded_tco2e,
    CASE
        WHEN p.expected_abatement_tco2e IS NULL OR p.expected_abatement_tco2e = 0 THEN NULL
        ELSE (COALESCE(SUM(a.actual_abatement_tco2e), 0) / p.expected_abatement_tco2e) * 100
    END AS abatement_progress_pct
FROM decarbonization_projects p
LEFT JOIN fact_project_abatement a ON a.project_id = p.id
GROUP BY p.tenant_id, p.id, p.name, p.category, p.status, p.planned_start_date, p.planned_end_date,
         p.expected_abatement_tco2e, p.actual_abatement_tco2e;

CREATE INDEX IF NOT EXISTS mv_project_progress_tenant_status_idx
    ON mv_project_progress (tenant_id, status, project_id);
