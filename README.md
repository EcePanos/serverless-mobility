# Serverless Mobility

This repository contains PoCs for a public transport analytics system using serverless technologies.

## Prerequisites

- Docker

## Usage

```
docker compose up
```
A Grafana dashboard is provided for monitoring the demo.

## Description


This demo includes the following components:

- 2 Simulated IoT devices (Python), each pretending to be a sensor measuring the number of people in a bus.
- A message queue (RabbitMQ), where the IoT devices publish their messages.
- A message preprocessor (Python), that receives the messages from the queue and stores them in the cache.
- A cache (Redis), where the preprocessor stores the messages.
- A simulated data fusion engine (Python), that receives the messages from the cache, calculates the bus occupancy by averaging the values received from the sensors, and stores the results in the database.
- A database (PostgreSQL with the TimescaleDB plugin), where the data fusion engine stores the results.
- A Grafana dashboard, where the results are visualized.

## Known issues

- When using the new version of Docker compose, after shutting down the demo, the Docker CLI will hang, needing to force quit.