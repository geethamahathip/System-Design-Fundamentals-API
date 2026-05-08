from sqlalchemy import Column, Integer, String, DateTime, Index
from app.db import Base
from datetime import datetime
class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(String, nullable=False)
    code = Column(String, nullable=False)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    __table_args__ = (
        Index("ix_links_created_by", "created_by"),
        Index("ix_links_tenant_code","tenant_id","code",unique=True),
    )
