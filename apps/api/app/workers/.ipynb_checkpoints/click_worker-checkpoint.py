import json
import time
from app.cache.redis_client import client
from app.db import SessionLocal
from app.models.click_event import ClickEvent
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy.exc import IntegrityError

QUEUE_KEY = "click_events"
def process_event(data, db):
    # FIX: ensure datetime conversion (tests pass string)
    ts = data["timestamp"]
    if isinstance(ts, str):
        ts = datetime.fromisoformat(ts)
    event = ClickEvent(
        event_id=data["event_id"],
        tenant_id=data["tenant_id"],
        link_id=data["link_id"],
        timestamp=ts,
        clicked_at=ts,
        user_agent=data.get("user_agent"),
        referrer=data.get("referrer"),
        ip_hash=data.get("ip_hash"),
    )
    db.add(event)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return
        
def start_click_worker():
    print("CLICK WORKER STARTED")

    while True:
        try:
            item = client.brpop(QUEUE_KEY, timeout=5)

            if not item:
                continue

            _, raw = item
            data = json.loads(raw)

            db = SessionLocal()

            try:
                process_event(data, db)
                print("CLICK_WRITTEN:", data["event_id"])
            except Exception as e:
                db.rollback()
                print("CLICK_WRITE_FAILED:", str(e))
            finally:
                db.close()

        except Exception as e:
            print("WORKER_ERROR:", str(e))
            time.sleep(1)


if __name__ == "__main__":
    start_click_worker()