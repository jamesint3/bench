from __future__ import annotations

import os
import time

import psycopg2


def _env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


host = _env("GEXABLE_DB_HOST", "localhost")
port = int(_env("GEXABLE_DB_PORT", "5432"))
dbname = _env("GEXABLE_DB_NAME", "gexable_esg")
user = _env("GEXABLE_DB_USER", "gexable")
password = _env("GEXABLE_DB_PASSWORD", "gexable")

for attempt in range(1, 31):
    try:
        conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
        conn.close()
        print(f"Database is ready on attempt {attempt}")
        raise SystemExit(0)
    except psycopg2.OperationalError as exc:
        print(f"Waiting for database ({attempt}/30): {exc}")
        time.sleep(2)

raise SystemExit("Database did not become ready after 60 seconds")
