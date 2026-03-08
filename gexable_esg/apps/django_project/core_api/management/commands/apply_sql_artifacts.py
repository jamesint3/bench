from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import DatabaseError, connection


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

        skipped_files: list[Path] = []
        connection.ensure_connection()
        with connection.cursor() as cursor:
            for sql_file in sql_files:
                self.stdout.write(f"Applying {sql_file.relative_to(root.parent)}")
                try:
                    cursor.execute(sql_file.read_text())
                except DatabaseError as exc:
                    message = str(exc)
                    if "timescaledb.control" in message:
                        skipped_files.append(sql_file)
                        self.stdout.write(
                            self.style.WARNING(
                                "Skipping SQL artifact because TimescaleDB is unavailable: "
                                f"{sql_file.relative_to(root.parent)}"
                            )
                        )
                        continue
                    raise

        if skipped_files:
            self.stdout.write(
                self.style.WARNING(
                    f"Applied {len(sql_files) - len(skipped_files)} SQL artifact files; "
                    f"skipped {len(skipped_files)} TimescaleDB-dependent file(s)."
                )
            )
            return

        self.stdout.write(self.style.SUCCESS(f"Applied {len(sql_files)} SQL artifact files."))
