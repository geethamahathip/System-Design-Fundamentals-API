from app.db import SessionLocal
from app.models.link import Link


def test_redirect(client):
    db = SessionLocal()

    existing = db.query(Link).filter(Link.code == "hSDR4ASM").first()

    if not existing:
        link = Link(
            tenant_id="t1",
            code="hSDR4ASM",
            long_url="https://google.com",
            created_by="user1",
        )
        db.add(link)
        db.commit()

    db.close()

    res = client.get("/r/hSDR4ASM", follow_redirects=False)

    assert res.status_code in (307, 302)