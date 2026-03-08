# Gexable ESG — Next Actions for App Development

This plan translates the current Django scaffold into a production-ready ESG platform through phased, concrete deliverables.

## Implementation Status (current)

- ✅ Week 0 started: settings split (`base/dev/prod`), `.env.example`, and initial baseline structure are in place.
- ✅ Week 1 started: API versioning (`/api/v1`), validation helpers, and standardized error responses are implemented.
- ✅ Week 2 started: core persistence models, initial migration, repositories, and audit logging hooks are added.
- ✅ Week 1 progressed: DRF APIViews, serializers, standardized validation responses, and OpenAPI/Swagger endpoints (`/api/v1/schema`, `/api/v1/docs`) are added.
- ✅ Week 3 started: transactional outbox table (`DomainEventOutbox`) and repository stub for publish lifecycle are added.
- ✅ Week 4 started: tenant context middleware, role-based API permissions, and outbox publisher management command are added.
- ⏭️ Remaining items below are still planned and should be completed in subsequent iterations.

## 0) Immediate Baseline Hardening (Week 1)

1. **Dependency and runtime stability**
   - Ensure Django dependency installs in CI and dev images.
   - Pin app dependencies and add lockfile strategy.
2. **Project health gates**
   - Add CI jobs for lint, unit tests, and type checks.
   - Fail CI on formatting/lint violations.
3. **Environment config**
   - Add `.env.example` and split settings (`base/dev/prod`).
   - Move secrets to env vars only.

## 1) API and Validation Foundation (Weeks 1–2)

1. **Adopt Django REST Framework (DRF)**
   - Replace raw JSON views with DRF `APIView`/`ViewSet`.
   - Add request/response serializers for all endpoints.
2. **Input validation and error model**
   - Enforce schema validation (units, quantity > 0, required IDs).
   - Standardize error response format with traceable codes.
3. **API versioning and docs**
   - Introduce `/api/v1/...` routing.
   - Auto-generate OpenAPI/Swagger and publish examples.

## 2) Persistence and Domain Modeling (Weeks 2–4)

1. **Create Django models (minimum set)**
   - `Organization`, `Site`, `ActivityRecord`, `EmissionFactor`, `EmissionResult`, `DisclosureReport`, `AuditLog`.
2. **Database migrations and indexing**
   - Add migrations with indexes on tenant, site, period, and timestamps.
   - Add idempotency keys for ingestion requests.
3. **Repository/service boundaries**
   - Move from in-memory flow to repository-backed services.
   - Keep services deterministic and side-effect boundaries explicit.

## 3) Eventing and Workflow Reliability (Weeks 3–5)

1. **Transactional outbox pattern**
   - Persist domain events with business writes.
   - Add worker to publish events reliably.
2. **Workflow state machine**
   - Implement robust transitions for draft/review/approved/closed.
   - Add role-based guards on transitions.
3. **Audit and lineage**
   - Attach `source_ref`, `ingested_by`, `calculation_method_version`, `factor_version` to every result.

## 4) Calculation Engine Evolution (Weeks 4–6)

1. **Scope engine expansion**
   - Extend from basic scope logic to configurable Scope 1/2/3 calculators.
2. **Versioned factors and methods**
   - Store factor tables with validity windows and source metadata.
3. **Recalculation strategy**
   - Add batch recalculation endpoint when factors/methods change.
   - Ensure reproducibility with method+factor snapshots.

## 5) Governance, Security, and Multi-tenancy (Weeks 4–7)

1. **AuthN/AuthZ**
   - Add SSO/OIDC integration and role model (preparer/reviewer/approver/admin).
2. **Tenant isolation**
   - Enforce tenant filters in repositories/querysets.
   - Add middleware for tenant context resolution.
3. **Governance controls**
   - Implement approval chains for disclosure publication.
   - Introduce immutable audit logs and evidence attachments.

## 6) Reporting and Disclosure Packs (Weeks 6–8)

1. **Framework adapters**
   - Start with CSRD and GHG Protocol output mappers.
2. **Export pipeline**
   - Generate CSV/XLSX/JSON packs with versioned report snapshots.
3. **Evidence binder**
   - Link report metrics to source records and supporting documents.

## 7) Observability and Operational Readiness (Weeks 6–8)

1. **Telemetry**
   - Add structured logging, request IDs, and event correlation IDs.
2. **SLOs and alerts**
   - Define ingestion latency, calculation success rate, and report publish success SLOs.
3. **Runbooks**
   - Add incident runbooks for failed ingestion, event backlog, and recalculation failures.

## 8) Test Strategy Expansion (Ongoing)

1. **Unit tests** for validators, calculators, and workflow guards.
2. **API contract tests** for request/response schemas.
3. **Integration tests** with DB + outbox + worker.
4. **Golden dataset tests** for reproducible emissions outputs.

## 9) Suggested Backlog (Top 12 Tickets)

1. Add DRF and convert existing endpoints to serializer-backed views.
2. Add API version prefix `/api/v1`.
3. Implement `Organization` and `Site` Django models with migrations.
4. Implement `ActivityRecord` model and ingestion persistence.
5. Add `EmissionFactor` + `EmissionResult` models and service persistence.
6. Build standardized error handling middleware.
7. Add tenant middleware and tenant-scoped queryset helpers.
8. Add `AuditLog` model and write audit entries in publish/calculate paths.
9. Implement outbox event table + publisher worker stub.
10. Add CSRD export endpoint (`/disclosures/export/csrd`).
11. Add approval workflow endpoint (`/disclosures/{id}/submit-review`).
12. Add CI checks: pytest, ruff/flake8, mypy (or pyright), and coverage threshold.

## Definition of Done for MVP Milestone

- Persistent ingestion and emissions results (no in-memory-only critical paths).
- Tenant-aware authorization on all write endpoints.
- Repeatable emissions calculation with versioned factors.
- One disclosure framework export with evidence links.
- Auditability from source record to reported metric.
