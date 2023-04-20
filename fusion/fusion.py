# Every minute, retrieve the keys from Redis
import sys
import redis
import time
import psycopg2
import os


# get redis host from environment variable
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", 6379)

# get postgres host from environment variable
postgres_host = os.environ.get("POSTGRES_HOST", "localhost")
postgres_port = os.environ.get("POSTGRES_PORT", 5432)
postgres_db = os.environ.get("POSTGRES_DB", "bus_data")
postgres_user = os.environ.get("POSTGRES_USER", "my_user")
postgres_password = os.environ.get("POSTGRES_PASSWORD", "my_password")

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
# Clear the Redis database
redis_client.flushdb()
# Connect to TimescaleDB
conn = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database=postgres_db,
    user=postgres_user,
    password=postgres_password
)
cur = conn.cursor()


while True:
    try:
        redis_keys = redis_client.keys()
        #print(f"Keys: {redis_keys}")
        # Group the keys by vehicle ID
        vehicle_ids = {}
        for key in redis_keys:
            key = key.decode('utf-8')
            vehicle_id = key.split('_')[0]
            if vehicle_id not in vehicle_ids:
                vehicle_ids[vehicle_id] = []
            vehicle_ids[vehicle_id].append(key)
        # For each vehicle ID, retrieve the values from Redis and calculate the average passenger count
        for vehicle_id in vehicle_ids:
            passenger_counts = []
            for key in vehicle_ids[vehicle_id]:
                passenger_count = int(redis_client.get(key).decode('utf-8').split('_')[0])
                passenger_counts.append(passenger_count)
            average_passenger_count = sum(passenger_counts) / len(passenger_counts)
            # Round the average passenger count to the nearest integer
            average_passenger_count = round(average_passenger_count)
            print(f"Passenger count for vehicle {vehicle_id}: {average_passenger_count}")
            # Persist the average passenger count to TimescaleDB with the vehicle ID and the current timestamp
            cur.execute(f"INSERT INTO occupancy (vehicle_id, passenger_count, timestamp) VALUES ('{vehicle_id}', {average_passenger_count}, NOW())")
            conn.commit()


        time.sleep(2)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            conn.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)