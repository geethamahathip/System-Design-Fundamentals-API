from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.db import SessionLocal
from app.models.link import Link
from app.cache.redis_client import get_redirect, set_redirect, client
from app.services.analytics_service import create_click_event
import uuid
import hashlib
import json
from datetime import datetime

router = APIRouter()
QUEUE_KEY="click_events"

LIMIT = 20
request_count = {}


def hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()


@router.get("/r/{code}")
def redirect(code: str, request: Request):
    db = SessionLocal()

    try:
        request_count[code] = request_count.get(code, 0) + 1

        if request_count[code] > LIMIT:
            raise HTTPException(status_code=429, detail="Too Many Requests")

        cached = get_redirect(code)
        if cached:
            return RedirectResponse(url=cached, status_code=307)

        link = db.query(Link).filter(Link.code == code).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        set_redirect(code, link.long_url)

        event_id = str(uuid.uuid4())

        payload = {
            "event_id": event_id,
            "tenant_id": link.tenant_id,
            "link_id": link.id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_agent": request.headers.get("user-agent"),
            "referrer": request.headers.get("referer"),
            "ip_hash": hash_ip(request.client.host),
        }

        try:
            print("ABOUT_TO_ENQUEUE:", event_id)
        
            print("REDIS_CLIENT_OBJECT:", client)
        
            client.rpush(QUEUE_KEY, json.dumps(payload))
        
            print("CLICK_ENQUEUED:", event_id)
        
        except Exception as e:
            print("QUEUE_FAILED:", repr(e))

        return RedirectResponse(url=link.long_url)

    finally:
        db.close()