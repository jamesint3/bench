CREATE MATERIALIZED VIEW IF NOT EXISTS mv_audit_closure_trend AS
SELECT
    f.tenant_id,
    date_trunc('month', COALESCE(f.due_date, a.audit_date))::date AS month_start,
    COUNT(*) AS total_findings,
    COUNT(*) FILTER (WHERE f.status = 'closed') AS closed_findings,
    COUNT(*) FILTER (WHERE f.status <> 'closed') AS open_findings,
    CASE WHEN COUNT(*) = 0 THEN 0
         ELSE (COUNT(*) FILTER (WHERE f.status = 'closed')::numeric / COUNT(*)::numeric) * 100
    END AS closure_rate_pct
FROM audit_findings f
JOIN audits a ON a.id = f.audit_id
GROUP BY f.tenant_id, date_trunc('month', COALESCE(f.due_date, a.audit_date))::date;

CREATE INDEX IF NOT EXISTS mv_audit_closure_trend_tenant_month_idx
    ON mv_audit_closure_trend (tenant_id, month_start);
