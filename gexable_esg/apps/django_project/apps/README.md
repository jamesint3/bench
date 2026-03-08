# Backend app boundaries

Each app should follow this internal shape:

- `models.py`: schema
- `services.py`: write/business logic
- `selectors.py`: read/query logic
- `tasks.py`: celery jobs
- `serializers.py`: api contracts
- `views.py`: delivery controllers
- `urls.py`: endpoint routes
- `permissions.py`: module permissions
- `filters.py`: query filters

Recommended apps:

- `core`, `tenants`, `users`, `permissions`, `audit_log`
- `data_ingestion`, `emissions_management`, `energy_management`
- `decarbonization`, `supplier_intelligence`, `audits_actions`
- `analytics`, `reporting`, `dashboard_api`
