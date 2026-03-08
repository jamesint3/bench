-- TimescaleDB setup for raw interval-heavy tables.
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Keep raw interval data in hypertables.
SELECT create_hypertable('meter_readings_raw', 'reading_timestamp', if_not_exists => TRUE);
SELECT create_hypertable('renewable_generation_raw', 'reading_timestamp', if_not_exists => TRUE);
SELECT create_hypertable('battery_dispatch_raw', 'event_timestamp', if_not_exists => TRUE);

-- Recommended compression policy placeholders (tune per environment):
-- ALTER TABLE meter_readings_raw SET (timescaledb.compress, timescaledb.compress_segmentby = 'tenant_id,meter_id');
-- SELECT add_compression_policy('meter_readings_raw', INTERVAL '30 days');
