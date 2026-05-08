from datetime import datetime
from typing import Optional, List
from urllib.parse import urlparse
from pydantic import BaseModel, field_validator
class CreateLinkRequest(BaseModel):
    long_url: str
    code: Optional[str] = None
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = []
    @field_validator("long_url")
    @classmethod
    def validate_long_url(cls, value: str) -> str:
        value = value.strip()
        if any(ord(ch) < 32 for ch in value):
            raise ValueError("URL contains invalid control characters")
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("URL scheme must be http or https")
        if not parsed.netloc:
            raise ValueError("URL must include a host")
        return value
class UpdateLinkRequest(BaseModel):
    long_url: Optional[str] = None
    code: Optional[str] = None
    expires_at: Optional[datetime] = None