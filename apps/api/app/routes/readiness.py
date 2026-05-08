from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from app.db import SessionLocal
from app.cache.redis_client import client

router = APIRouter()

@router.get("/ready")
def readiness_check():
    db = SessionLocal()

    try:
        # DB check
        db.execute(text("SELECT 1"))

        # Redis check
        client.ping()

        return {"status": "ready"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Dependencies unavailable"
        )

    finally:
        db.close()