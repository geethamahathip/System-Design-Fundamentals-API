def test_click_idempotency(db):
    from app.workers.click_worker import process_event

    payload = {
        "event_id": "same-id",
        "tenant_id": "t1",
        "link_id": 1,
        "timestamp": "2026-01-01T00:00:00",
        "user_agent": "test",
        "referrer": None,
        "ip_hash": "abc"
    }

    process_event(payload, db)
    process_event(payload, db)

    from app.models.click_event import ClickEvent

    count = db.query(ClickEvent).filter_by(event_id="same-id").count()
    assert count == 1