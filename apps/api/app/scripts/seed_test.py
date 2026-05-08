from app.db import SessionLocal
from app.models.link import Link
from app.models.click_event import ClickEvent
db = SessionLocal()
try:
#create link
    link = db.query(Link).filter_by(code="abc123").first()

    if not link:
        link = Link(
            tenant_id="t1",
            code="abc123",
            long_url="https://example.com",
            created_by="user1"
        )
        db.add(link)
        db.commit()
        db.refresh(link)
        print("LINK_CREATED")
    else:
        print("LINK_EXISTS")
#create click
    click = db.query(ClickEvent).filter_by(event_id="seed-click-1").first()

    if not click:
        click = ClickEvent(
            event_id="seed-click-1",
            tenant_id="t1",
            link_id=link.id,
            user_agent="test-browser",
            referrer="google",
            ip_hash="xyz"
        )
        db.add(click)
        db.commit()
        print("CLICK_CREATED")
    else:
        print("CLICK_EXISTS")
#proof query
    result = db.query(Link).filter_by(code="abc123").first()
    print("REDIRECT RESULT:", result.long_url)

    clicks = db.query(ClickEvent).filter_by(link_id=link.id).all()
    print("CLICK COUNT:", len(clicks))

except Exception as e:
    db.rollback()
    print("SEED_ERROR:", str(e))

finally:
    db.close()