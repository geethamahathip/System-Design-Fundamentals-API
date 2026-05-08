from app.db import SessionLocal
from app.services.analytics_service import purge_old_clicks

if __name__ == "__main__":
    db = SessionLocal()
    deleted = purge_old_clicks(db)
    print("PURGED_CLICKS:", deleted)
    db.close()