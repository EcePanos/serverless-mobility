# connect to redis and list all keys
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_keys = redis_client.keys()
print(f"Keys: {redis_keys}")