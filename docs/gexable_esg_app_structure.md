# ESG Application Structure (Gexable ESG Capability Coverage)

This document proposes a production-ready application structure for an ESG platform that covers core capabilities similar to Gexable ESG product functions: data capture, emissions accounting, target tracking, analytics, disclosures, and governance controls.

## 1) Capability Map

| Capability Area | What it Covers | Suggested Module |
|---|---|---|
| Enterprise Data Foundation | Utility bills, meter reads, ERP/AP extracts, supplier uploads, APIs | `modules/data_foundation` |
| Emissions Management | Scope 1/2/3 calculations, factors, methodologies, recalculation logic | `modules/emissions` |
| Energy & Sustainability Performance | Energy intensity, facility performance, benchmarking | `modules/performance` |
| Decarbonization Planning | Abatement projects, MAC curves, scenarios, target plans | `modules/decarbonization` |
| Reporting & Disclosures | CSRD/ISSB/GRI/CDP/SEC outputs, evidence trails, versioned reporting | `modules/reporting` |
| Audit & Compliance | Controls, approvals, evidence attachments, change logs | `modules/governance` |
| Master Data & Org Hierarchy | Legal entities, sites, assets, cost centers, ownership history | `modules/master_data` |
| Workflow & Collaboration | Tasks, reminders, review/approval chains | `modules/workflow` |
| Supplier & Value Chain | Supplier questionnaires, Scope 3 activity data, quality scoring | `modules/supplier` |
| Insights & AI | Hotspot detection, anomaly alerts, narrative generation | `modules/insights` |

## 2) Recommended Monorepo Layout

```text
gexable-esg-platform/
├── apps/
│   ├── web/                      # React/Next.js UI
│   ├── admin/                    # Internal admin UI
│   ├── api-gateway/              # Public API composition layer
│   └── worker/                   # Async jobs / schedulers
├── modules/
│   ├── data_foundation/
│   │   ├── ingestion/
│   │   ├── normalization/
│   │   ├── data_quality/
│   │   └── connectors/
│   ├── master_data/
│   ├── emissions/
│   │   ├── factors/
│   │   ├── calculators/
│   │   ├── scope1/
│   │   ├── scope2/
│   │   ├── scope3/
│   │   └── assurance/
│   ├── performance/
│   ├── decarbonization/
│   ├── reporting/
│   │   ├── frameworks/
│   │   ├── templates/
│   │   └── exports/
│   ├── governance/
│   ├── workflow/
│   ├── supplier/
│   └── insights/
├── platform/
│   ├── auth/                     # SSO, RBAC, ABAC policies
│   ├── tenancy/                  # Multi-tenant isolation
│   ├── observability/            # Logs, traces, ESG-specific metrics
│   ├── event_bus/                # Domain events + message contracts
│   └── feature_flags/
├── data/
│   ├── schemas/
│   ├── reference_data/
│   └── migrations/
├── infra/
│   ├── terraform/
│   ├── k8s/
│   └── ci/
├── docs/
│   ├── architecture/
│   ├── data_dictionary/
│   └── controls/
└── tests/
    ├── contract/
    ├── integration/
    └── e2e/
```

## 3) Domain-Driven Module Contracts

Each module should expose:

1. `api/` (commands/queries)
2. `domain/` (entities, value objects, rules)
3. `application/` (orchestration/use-cases)
4. `infrastructure/` (DB, queue, external adapters)
5. `events/` (published/subscribed events)

Example (emissions):

```text
modules/emissions/
├── api/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   └── services/
├── application/
├── infrastructure/
│   ├── repositories/
│   └── factor_providers/
└── events/
```

## 4) Core Data Objects (Minimum Set)

- `Organization`, `BusinessUnit`, `Site`, `Asset`
- `Meter`, `UtilityAccount`, `Invoice`, `ActivityRecord`
- `EmissionFactor`, `CalculationMethod`, `EmissionResult`
- `ReductionProject`, `Target`, `Scenario`
- `DisclosureReport`, `DisclosureMetric`, `EvidenceFile`
- `Control`, `Approval`, `AuditLog`
- `Supplier`, `SupplierResponse`, `Scope3Category`

## 5) Service Boundaries (Suggested)

- **Data Intake Service**: validates, maps, and lands incoming ESG activity data.
- **Calculation Service**: deterministic emissions engine with versioned factors and methods.
- **Performance Service**: KPI and trend aggregations across site/region/business unit.
- **Reporting Service**: disclosure dataset builder + template renderer + export.
- **Governance Service**: controls, approvals, and complete traceability.
- **Workflow Service**: tasks and state transitions for monthly/quarterly cycles.
- **Supplier Service**: value-chain collection and quality scoring.

## 6) Event Model (Examples)

- `activity_record.ingested`
- `activity_record.validated`
- `emission_result.calculated`
- `target.progress_updated`
- `disclosure.report_published`
- `control.exception_detected`

Use immutable events with schema versioning to support backfills and assurance.

## 7) Security & Governance Baseline

- Tenant-aware row-level security.
- Segregation of duties for preparer/reviewer/approver roles.
- Full data lineage from source file/API payload to reported metric.
- Immutable audit trails for calculation factor/method updates.
- PII minimization and retention policies by region.

## 8) Delivery Roadmap (Pragmatic)

### Phase 1 (Foundation)
- Master data hierarchy
- Data ingestion + validation
- Scope 1/2 calculation engine
- Baseline dashboards

### Phase 2 (Scale)
- Scope 3 categories
- Supplier portal/questionnaires
- Target tracking and abatement planning
- Workflow + approvals

### Phase 3 (Disclosure & Assurance)
- Multi-framework reporting packs
- Evidence binder automation
- Advanced anomaly detection and forecast insights

## 9) Starter Technology Choices

- **Backend:** Python (Django/DRF or FastAPI) or Node (NestJS)
- **Data processing:** Python workers + queue (Celery/RQ/Kafka)
- **Storage:** PostgreSQL + object storage for evidence/files
- **Analytics:** dbt + warehouse (BigQuery/Snowflake/Redshift)
- **Frontend:** React/Next.js with role-based route guards
- **Auth:** OIDC/SAML SSO + SCIM provisioning

---

This structure is intended as a robust starting point. You can slim it down for an MVP by combining modules (`governance + workflow`, `performance + insights`) and extracting them later as usage scales.
