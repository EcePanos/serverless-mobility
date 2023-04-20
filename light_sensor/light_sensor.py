import datetime
import json
import os
import random
import sys
import time

import pika

# Repeat every 5 seconds

# Get rabbitmq host from environment variable
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")

while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        passenger_count = random.randint(0, 100)

        # Create a message with the passenger count, vehicle ID, and current datetime as Unix timestamp
        message = {
            "passenger_count": passenger_count,
            "vehicle_id": "v1",
            "timestamp": datetime.datetime.now().timestamp(),
            "type": "light_sensor"
        }
        # Publich the message to RabbitMQ
        channel.basic_publish(exchange='', routing_key='occupancy', body=json.dumps(message))
        print(f"Sent message: {message}")
        connection.close()
        time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    
