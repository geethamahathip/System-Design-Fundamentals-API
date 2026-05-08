from datetime import datetime, timedelta
from app.models.click_event import ClickEvent
from sqlalchemy.orm import Session

RETENTION_DAYS = 30
def purge_old_clicks(db):
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    deleted = (
        db.query(ClickEvent)
        .filter(ClickEvent.clicked_at < cutoff)
        .delete(synchronize_session=False)
    )

    db.commit()
    return deleted
def create_click_event(
    db: Session,
    *,
    event_id: str,
    tenant_id: int,
    link_id: int,
    user_agent: str = None,
    referrer: str = None,
    ip_hash: str = None,
):
    event = ClickEvent(
        event_id=event_id,
        tenant_id=tenant_id,
        link_id=link_id,
        timestamp=datetime.utcnow(),
        clicked_at=datetime.utcnow(),
        user_agent=user_agent,
        referrer=referrer,
        ip_hash=ip_hash,
    )

    db.add(event)
    db.commit()