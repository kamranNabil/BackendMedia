import redis
import os
from redis import RedisError

# Use the environment variable with fallback
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Optional: Test connection
try:
    redis_client.ping()
    print("Connected to Redis successfully!")
except redis.exceptions.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")