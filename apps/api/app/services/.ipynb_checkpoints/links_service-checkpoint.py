import secrets
import string
import logging
import app.config as config
from app.models.link import Link
from app.db import SessionLocal
from app.schemas.link import CreateLinkRequest
import app.config as config

logger = logging.getLogger("app")


def generate_code(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_link(payload: CreateLinkRequest, tenant_id: str) -> Link:
    db = SessionLocal()

    try:
        # ✅ controlled failure
        if config.FORCE_DB_ERROR:
            raise RuntimeError("Simulated DB failure in write path")

        code = payload.code or generate_code()

        link = Link(
            tenant_id=tenant_id,
            code=code,
            long_url=payload.long_url,
            created_by=tenant_id,
            expires_at=payload.expires_at,
        )

        db.add(link)
        db.commit()
        db.refresh(link)

        return link

    except Exception as e:
        db.rollback()

        logger.error(
            "db_write_failed",
            extra={
                "error": str(e),
                "tenant_id": tenant_id,
                "operation": "create_link",
            }
        )

        # IMPORTANT: rethrow as-is (do NOT wrap here)
        raise

    finally:
        db.close()