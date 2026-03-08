from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Apply TimescaleDB and materialized view SQL artifacts to the active database."

    def handle(self, *args, **options):
        root = Path(__file__).resolve().parents[3] / "db" / "sql"
        ordered_dirs = [
            root / "functions",
            root / "materialized_views",
            root / "indexes",
        ]

        sql_files: list[Path] = []
        for sql_dir in ordered_dirs:
            sql_files.extend(sorted(sql_dir.glob("*.sql")))

        if not sql_files:
            self.stdout.write(self.style.WARNING("No SQL artifacts found to apply."))
            return

        connection.ensure_connection()
        with connection.cursor() as cursor:
            for sql_file in sql_files:
                self.stdout.write(f"Applying {sql_file.relative_to(root.parent)}")
                cursor.execute(sql_file.read_text())

        self.stdout.write(self.style.SUCCESS(f"Applied {len(sql_files)} SQL artifact files."))
