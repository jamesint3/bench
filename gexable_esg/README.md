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
