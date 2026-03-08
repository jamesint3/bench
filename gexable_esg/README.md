# Gexable ESG Starter Code (Django Base)

This starter package uses a Django base application for ESG APIs, now with baseline hardening and early persistence groundwork:

- Split environment-aware settings (`base/dev/prod`) and `.env.example`.
- Versioned API routes under `/api/v1`.
- Input validation + standardized error responses.
- Initial persistence models and repositories for core ESG domain objects.
- In-memory event bus retained for event-driven service flow.

## Run locally

```bash
python gexable_esg/apps/django_project/manage.py migrate
python gexable_esg/apps/django_project/manage.py runserver
```

## API endpoints

- `GET /api/v1/health`
- `POST /api/v1/activity-records`
- `POST /api/v1/emissions/calculate`
- `POST /api/v1/disclosures/publish`
- `GET /api/v1/audit/events`
- `GET /api/v1/schema` (OpenAPI schema)
- `GET /api/v1/docs` (Swagger UI)

> Note: persistence for `activity-records` and `emissions/calculate` requires numeric DB foreign keys (`site_id`, `activity_record_id`) to store records.

## Development plan

See `docs/gexable_esg_next_actions.md` for phased next actions and MVP backlog.


## Working demo

Run a complete in-memory demo flow (ingestion → emissions → disclosure → governance event):

```bash
python -m gexable_esg.demo.run_demo
```

This prints a JSON payload with created artifacts and emitted domain events.

Generate deterministic demo data for all Django business modules (tenants/users/permissions, ingestion, emissions, energy, supplier, decarbonization, audits, analytics, reporting):

```bash
python gexable_esg/demo/generate_demo_data.py
```

This writes:

- `gexable_esg/demo/demo_data_fixture.json` (Django fixture records)
- `gexable_esg/demo/dashboard_api_demo_payloads.json` (dashboard endpoint sample payloads)


## Docker demo (one command)

From the repository root, run:

```bash
docker compose up --build
```

### Step-by-step (Windows + Visual Studio / VS Code)

1. Open Docker Desktop and wait until it shows **Engine running**.
2. Open this repository folder (the one containing `Dockerfile` and `docker-compose.yml`) in Visual Studio/VS Code.
3. Open an integrated terminal in that root folder.
4. Run:

   ```bash
   docker compose up --build
   ```

5. Wait for log output similar to: `Starting development server at http://0.0.0.0:8000/`.
6. Open your browser at `http://localhost:8000/api/v1/health`.

If you change code and want a clean rebuild:

```bash
docker compose down
docker compose up --build --force-recreate
```

If you previously saw `ModuleNotFoundError: No module named 'gexable_esg'`, run a no-cache rebuild:

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

Then open:

- Main App (React): `http://localhost:8000/`
- Emissions Page: `http://localhost:8000/emissions-overview`
- Scope Trends: `http://localhost:8000/scope-trends`
- Energy by Site: `http://localhost:8000/energy-by-site`
- Tariff Analysis: `http://localhost:8000/tariff-analysis`
- Renewable Performance: `http://localhost:8000/renewable-performance`
- Decarbonization Projects: `http://localhost:8000/decarbonization-projects`
- Supplier Benchmarking: `http://localhost:8000/supplier-benchmarking`
- Audit Actions: `http://localhost:8000/audit-actions`
- Legacy demo pages: `http://localhost:8000/demo/ui/data-intake` (and other `demo/ui/*` routes)
- Django Admin: `http://localhost:8000/admin/`
- API Health: `http://localhost:8000/api/v1/health`

Quick API smoke tests:

```bash
curl -s http://localhost:8000/api/v1/health
curl -s -X POST http://localhost:8000/api/v1/activity-records \
  -H "Content-Type: application/json" \
  -d '{"site_id":"site-berlin-01","quantity":1200,"unit":"kWh"}'
curl -s http://localhost:8000/api/v1/audit/events
```

To stop:

```bash
docker compose down
```



### Using an existing Postgres container

If you already run Postgres outside this compose stack, use a Postgres 18+-safe data mount. Example:

```bash
docker run --name my_postgres \
  -e POSTGRES_PASSWORD=Polkmn001/* \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  -d postgres
```

Then keep it running and start only the app with DB overrides:

```bash
GEXABLE_DB_HOST=host.docker.internal \
GEXABLE_DB_PORT=5432 \
GEXABLE_DB_USER=postgres \
GEXABLE_DB_PASSWORD='Polkmn001/*' \
GEXABLE_DB_NAME=postgres \
GEXABLE_SECRET_KEY='replace-with-a-strong-secret' \
GEXABLE_ALLOWED_HOSTS='localhost,127.0.0.1' \
docker compose up --build --no-deps gexable-esg-app
```

On Windows `cmd.exe`, use quoted `set` syntax to avoid trailing spaces in env vars:

```bat
set "GEXABLE_DB_HOST=host.docker.internal" && ^
set "GEXABLE_DB_PORT=5432" && ^
set "GEXABLE_DB_USER=postgres" && ^
set "GEXABLE_DB_PASSWORD=Polkmn001/*" && ^
set "GEXABLE_DB_NAME=postgres" && ^
set "GEXABLE_SECRET_KEY=replace-with-a-strong-secret" && ^
set "GEXABLE_ALLOWED_HOSTS=localhost,127.0.0.1" && ^
docker compose up --build --no-deps gexable-esg-app
```

> Note: this compose file uses `/var/lib/postgresql` volume mounts (Postgres 18+ compatible) and no longer publishes TimescaleDB on host port `5432`, so it won't conflict with your existing container.

> Note: if you previously initialized data with `/var/lib/postgresql/data` on newer Postgres images, create a fresh volume or perform a proper `pg_upgrade` migration before reusing data.

> Note: if you see `could not translate host name "host.docker.internal "`, your env var likely contains a trailing space from `set VAR=value &&` usage in cmd; use `set "VAR=value"` as shown above.

> Note: when running against a plain PostgreSQL instance (without full Timescale/materialized-view prerequisites), runtime SQL artifacts that depend on unavailable extensions or missing base relations are skipped with warnings so the API can still boot.


## Dependency lock strategy

Use `gexable_esg/requirements-dev.lock` as the pinned dependency artifact for CI/dev reproducibility (generated via `pip-tools`).


## Tenant & role headers

API requests support:

- `X-Tenant-ID`: tenant scope context for request/queryset filtering.
- `X-User-Role`: one of `preparer`, `reviewer`, `approver`, `admin` for role-gated endpoints.

## Outbox publisher worker

Publish pending outbox events to the event bus:

```bash
python gexable_esg/apps/django_project/manage.py publish_outbox --once
```
