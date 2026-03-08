import time

from django.core.management.base import BaseCommand

from gexable_esg.apps.django_project.core_api.repositories import DomainEventOutboxRepository
from gexable_esg.apps.django_project.core_api.services import bus


class Command(BaseCommand):
    help = "Publish pending outbox events to the in-memory event bus."

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=100)
        parser.add_argument("--poll-seconds", type=float, default=2.0)
        parser.add_argument("--once", action="store_true", help="Process one batch and exit")

    def handle(self, *args, **options):
        repo = DomainEventOutboxRepository()
        batch_size = options["batch_size"]
        poll_seconds = options["poll_seconds"]
        run_once = options["once"]

        while True:
            pending = list(repo.get_pending(batch_size=batch_size))
            for event in pending:
                try:
                    bus.publish(
                        topic=event.topic,
                        payload=event.payload,
                        schema_version=event.schema_version,
                    )
                    repo.mark_published(event.id)
                except Exception as exc:  # noqa: BLE001
                    repo.mark_error(event.id, str(exc))

            if run_once:
                break

            if not pending:
                time.sleep(poll_seconds)
