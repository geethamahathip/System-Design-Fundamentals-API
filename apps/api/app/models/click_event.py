from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from app.db import Base
from datetime import datetime

class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, index=True)

    # idempotency key
    event_id = Column(String, unique=True, nullable=False, index=True)

    tenant_id = Column(Integer, nullable=False)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    clicked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_agent = Column(String, nullable=True)
    referrer = Column(String, nullable=True)
    ip_hash = Column(String, nullable=True)

    __table_args__ = (
        Index("ix_click_link_time", "link_id", "clicked_at"),
        Index("ix_click_tenant_time", "tenant_id", "clicked_at"),
    )