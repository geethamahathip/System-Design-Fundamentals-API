import logging
import redis
import app.config as config

logger = logging.getLogger("app")

REDIS_TIMEOUT_SEC = 2

client = redis.Redis.from_url(
    config.settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


def _key(code: str):
    return f"redirect:{code}"


def get_redirect(code: str):
    try:
        return client.get(_key(code))
    except Exception:
        logger.warning(f"redis_get_failed code={code}")
        return None


def set_redirect(code: str, long_url: str):
    try:
        client.set(_key(code), long_url)
    except Exception:
        logger.warning(f"redis_set_failed code={code}")


def delete_redirect(code: str):
    try:
        client.delete(_key(code))
    except Exception:
        logger.warning(f"redis_delete_failed code={code}")


def clear_all():
    try:
        client.flushdb()
    except Exception:
        pass