import json
from app.cache.redis_client import redis

QUEUE_KEY = "click_events"

def enqueue_click(event: dict):
    redis.lpush(QUEUE_KEY, json.dumps(event))