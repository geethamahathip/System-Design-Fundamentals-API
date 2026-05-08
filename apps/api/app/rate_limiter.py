import time
from collections import defaultdict
from fastapi import HTTPException

request_log = defaultdict(list)
WINDOW = 10


def check_rate_limit(key: str, limit: int = 20):
    now = time.time()

    request_log[key] = [
        t for t in request_log[key]
        if now - t < WINDOW
    ]

    if len(request_log[key]) >= limit:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    request_log[key].append(now)