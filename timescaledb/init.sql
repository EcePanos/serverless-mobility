--TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create hypertable for passenger counts
CREATE TABLE IF NOT EXISTS occupancy (
    timestamp TIMESTAMPTZ NOT NULL,
    vehicle_id TEXT NOT NULL,
    passenger_count INTEGER NOT NULL
);

SELECT create_hypertable('occupancy', 'timestamp');