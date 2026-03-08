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

> Note: persistence for `activity-records` and `emissions/calculate` requires numeric DB foreign keys (`site_id`, `activity_record_id`) to store records.

## Development plan

See `docs/gexable_esg_next_actions.md` for phased next actions and MVP backlog.


## Working demo

Run a complete in-memory demo flow (ingestion → emissions → disclosure → governance event):

```bash
python -m gexable_esg.demo.run_demo
```

This prints a JSON payload with created artifacts and emitted domain events.


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

- Health: `http://localhost:8000/api/v1/health`

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
