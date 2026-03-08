# Gexable ESG Commercial Blueprint (Non-invasive Scaffold)

This directory is an **implementation blueprint** for a commercial Django + React ESG platform.

- It is intentionally isolated under `blueprints/`.
- It does **not** modify the active runtime app in `gexable_esg/`.
- It provides a practical target structure, schema map, endpoint map, and starter model examples.

## Core Principle

`raw data -> processing jobs -> fact/kpi/materialized views -> API -> dashboards`

## Included

- `backend/`: recommended Django monorepo backend layout with app boundaries.
- `frontend/`: recommended React frontend module layout.
- `infra/`: docker/compose/k8s placeholder layout.
- `docs/`: architecture, API, and data-model blueprint docs.

## How to use

1. Use this as a migration roadmap, not as an in-place replacement.
2. Incrementally move existing code into these module boundaries.
3. Keep tenant isolation and role-based access explicit on all domain entities.
