# Gexable ESG Starter Code (Django Base)

This starter package now uses a Django base application for ESG APIs:

- Django project scaffold at `gexable_esg/apps/django_project`.
- API endpoints for data intake, emissions, reporting, and event audit.
- Service classes for each major ESG module section.
- In-memory event bus with versioned domain events.

## Run locally

```bash
python gexable_esg/apps/django_project/manage.py migrate
python gexable_esg/apps/django_project/manage.py runserver
```

## API endpoints

- `GET /api/health`
- `POST /api/activity-records`
- `POST /api/emissions/calculate`
- `POST /api/disclosures/publish`
- `GET /api/audit/events`

## Next implementation steps

1. Replace in-memory stores with repositories and PostgreSQL models.
2. Add authentication and tenant context middleware.
3. Introduce background workers for heavy ingestion and calculations.
4. Add framework-specific disclosure renderers.


## Development plan

See `docs/gexable_esg_next_actions.md` for phased next actions and MVP backlog.
