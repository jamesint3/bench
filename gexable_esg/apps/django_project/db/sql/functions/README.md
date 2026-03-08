# SQL function and platform scripts

This folder includes SQL scripts for database capabilities that support dashboard performance.

## Included

- `timescaledb_hypertables.sql`
  - enables TimescaleDB
  - creates hypertables for raw interval data:
    - `meter_readings_raw`
    - `renewable_generation_raw`
    - `battery_dispatch_raw`

## Rule

Do not query raw hypertables directly from dashboard APIs except for explicit drill-down endpoints.
Use aggregates/facts/materialized views for dashboard pages.
