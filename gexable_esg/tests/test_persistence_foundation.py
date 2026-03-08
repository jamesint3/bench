from pathlib import Path


def test_outbox_model_and_migration_exist() -> None:
    models = Path("gexable_esg/apps/django_project/core_api/models.py").read_text()
    migration = Path("gexable_esg/apps/django_project/core_api/migrations/0002_outbox_indexes.py").read_text()

    assert "class DomainEventOutbox" in models
    assert "CreateModel" in migration
    assert "DomainEventOutbox" in migration


def test_repository_contracts_include_outbox() -> None:
    repos = Path("gexable_esg/apps/django_project/core_api/repositories.py").read_text()
    assert "class DomainEventOutboxRepository" in repos
    assert "def queue" in repos
