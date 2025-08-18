import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Connect to Redis container
redis_client = redis.Redis(
    host="localhost",   # matches the docker-compose service name
    port=6379,
    decode_responses=True
)

# Optional: Test connection
try:
    redis_client.ping()
    print("Connected to Redis successfully!")
except redis.exceptions.ConnectionError:
    print("Failed to connect to Redis.")
