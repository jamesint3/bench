# Gexable ESG Commercial Blueprint (Non-invasive Scaffold)

This blueprint has been updated to mirror the requested commercial structure while remaining isolated from the active runtime under `gexable_esg/`.

## Scope and safety

- Lives entirely under `blueprints/gexable_esg_app/`.
- Does **not** change the current Django runtime entrypoints.
- Serves as a migration target for phased adoption.

## Current blueprint layout

```text
gexable_esg_app/
├── backend/
│   ├── manage.py
│   ├── pyproject.toml
│   ├── requirements/{base,dev,prod}.txt
│   ├── config/{urls,asgi,wsgi,celery}.py
│   ├── config/settings/{base,dev,prod}.py
│   ├── apps/
│   │   ├── core/
│   │   ├── tenants/
│   │   ├── users/
│   │   ├── permissions/
│   │   ├── audit_log/
│   │   ├── data_ingestion/
│   │   ├── emissions_management/
│   │   ├── energy_management/
│   │   ├── decarbonization/
│   │   ├── supplier_intelligence/
│   │   ├── audits_actions/
│   │   ├── analytics/
│   │   ├── reporting/
│   │   └── dashboard_api/
│   ├── modules/
│   ├── db/sql/{materialized_views,functions,indexes}
│   ├── db/seeds/
│   ├── scripts/
│   ├── tests/{unit,integration,api,analytics}
│   └── static/
├── frontend/
│   ├── package.json
│   ├── src/{app,pages,modules,components,charts,tables,hooks,services,store,utils,types}
│   └── public/
├── infra/
│   ├── docker/{backend.Dockerfile,frontend.Dockerfile,nginx.conf}
│   ├── compose/{docker-compose.dev.yml,docker-compose.prod.yml}
│   └── k8s/
├── docs/{architecture,api,data-model,product}
└── .env.example
```

## Design rule

`raw data -> processing jobs -> fact/kpi/materialized views -> API -> dashboard`
