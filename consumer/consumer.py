# Consume the messages from the queue

import sys
import pika
import json
import os

import redis

# get rabbitmq host from environment variable
rabbitmq_host = os.environ.get("RABBITMQ_HOST", "localhost")
# get redis host from environment variable
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", 6379)

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Create a queue for the consumer
    channel.queue_declare(queue='occupancy')

    # Create a Redis client
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

    # Define a callback function that will be called when a message is received
    def callback(ch, method, properties, body):
        # Parse the message body as JSON
        message = json.loads(body)
        # Persist the message to Redis, with the key being the combination of the vehicle ID and the type
        # and the value being the passenger count and the timestamp
        redis_client.set(f"{message['vehicle_id']}_{message['type']}", f"{message['passenger_count']}_{message['timestamp']}")
        print(f"Received message: {message}")
    # Start consuming messages
    channel.basic_consume(queue='occupancy', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)